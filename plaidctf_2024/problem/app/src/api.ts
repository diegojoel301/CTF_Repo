import bcrypt from "bcrypt";
import express from "express";
import * as nodemailer from "nodemailer";
import type SMTPTransport from "nodemailer/lib/smtp-transport/index.js";
import { sql } from "slonik";
import { z } from "zod";

import base64id from "./base64id.js";
import { ChatSession, InboundMessageSchema } from "./chat.js";
import { pool } from "./db.js";
import { env } from "./env.js";
import { Socket } from "./infra.js";
import { logger } from "./logger.js";

let emailTransportOptions: SMTPTransport.Options;

if (env.SENDGRID_API_KEY !== undefined && env.SENDGRID_API_KEY !== "") {
	emailTransportOptions = {
		host: "smtp.sendgrid.net",
		port: 465,
		secure: true,
		auth: {
			user: "apikey",
			pass: env.SENDGRID_API_KEY
		}
	};
} else {
	logger.warn("SENDGRID_API_KEY not set; using ethereal.email for email transport");
	const etherealAccount = await nodemailer.createTestAccount();
	logger.info({ etherealAccount }, "Ethereal account created");
	emailTransportOptions = {
		host: "smtp.ethereal.email",
		port: 465,
		secure: true,
		auth: {
			user: etherealAccount.user,
			pass: etherealAccount.pass
		}
	};
}

const emailTransport = nodemailer.createTransport(emailTransportOptions);

export const apiRouter = express.Router();
let sessions = new Map<string, ChatSession>();

apiRouter.use(async (req, res, next) => {
	req.werechat = {};

	if (typeof req.cookies.session === "string") {
		try {
			req.werechat.user = await pool.maybeOne(sql.type(z.object({ id: z.string(), settings: z.unknown() }))`
				SELECT *
				FROM werechat.user
					JOIN werechat.token ON werechat.token.user_id = werechat.user.id
				WHERE werechat.token.token = ${req.cookies.session}
			`) ?? undefined;
		} catch (err) {
			// Ignore
		}
	}

	next();
});

apiRouter.post("/register", async (req, res) => {
	await pool.transaction(async (tx) => {
		const body = z.object({
			inviteCode: z.string(),
			email: z.string().email(),
			username: z.string(),
			password: z.string(),
		}).parse(req.body);

		const inviteOk = await tx.maybeOne(sql.unsafe`
			DELETE FROM werechat.invite
			WHERE code = ${body.inviteCode}
			RETURNING *
		`);

		if (!inviteOk) {
			res.status(403).send("Invalid invite code");
			return;
		}

		const passwordHash = await bcrypt.hash(body.password, 12);

		await tx.one(sql.unsafe`
			INSERT INTO werechat.user (id, email, password)
			VALUES (${body.username}, ${body.email}, ${passwordHash})
			RETURNING *
		`);

		res.json({ success: true });
	});
});

apiRouter.post("/login", async (req, res) => {
	const body = z.object({
		username: z.string(),
		password: z.string(),
	}).parse(req.body);

	const user = await pool.maybeOne(sql.type(z.object({ id: z.string(), password: z.string() }))`
		SELECT * FROM werechat.user
		WHERE id = ${body.username}
	`);

	if (user === null) {
		res.status(403).send("Invalid username or password");
		return;
	}

	const passwordOk = await bcrypt.compare(body.password, user.password);

	if (!passwordOk) {
		res.status(403).send("Invalid username or password");
		return;
	}

	const token = await pool.one(sql.type(z.object({ token: z.string() }))`
		INSERT INTO werechat.token (user_id)
		VALUES (${user.id})
		RETURNING token
	`);

	res.cookie("session", token.token, { httpOnly: true });
	res.json({ success: true });
});

apiRouter.post("/logout", async (req, res) => {
	if (req.werechat.user === undefined) {
		res.status(403).send("Not authenticated");
		return;
	}

	await pool.query(sql.unsafe`
		DELETE FROM werechat.token
		WHERE user_id = ${req.werechat.user.id}
	`);

	res.clearCookie("session");
	res.json({ success: true });
});

apiRouter.post("/request-reset", async (req, res) => {
	const body = z.object({
		username: z.string(),
	}).parse(req.body);

	const user = await pool.maybeOne(sql.type(z.object({ id: z.string(), email: z.string() }))`
		SELECT id, email
		FROM werechat.user
		WHERE id = ${body.username}
	`);

	if (user === null) {
		res.status(403).send("Invalid username");
		return;
	}

	const requestedTooRecently = await pool.exists(sql.unsafe`
		SELECT 1
		FROM werechat.password_reset
		WHERE user_id = ${user.id} AND created_at > NOW() - INTERVAL '30 seconds'
	`);

	if (requestedTooRecently) {
		res.status(403).send("Reset already requested");
		return;
	}

	const resetCode = base64id(12);

	await pool.query(sql.unsafe`
		INSERT INTO werechat.password_reset (user_id, code)
		VALUES (${user.id}, ${resetCode})
	`);

	logger.info({ user: user.id, code: resetCode }, "Reset requested");
	emailTransport.sendMail({
		from: "noreply@werechat.chal.pwni.ng",
		to: user.email,
		subject: "Password reset",
		text: `
			You have requested a password reset for your account. Please visit the following link to reset your password:

			https://werechat.pwni.ng/reset?username=${user.id}&code=${resetCode}

			If you did not request this reset, please ignore this email.
		`.replace(/^\t+/gm, "").trim(),
	})
		.then((info) => logger.info({ info }, "Email sent"))
		.catch((err) => logger.error({ err }, "Error sending email"));

	res.json({ success: true });
});

apiRouter.post("/reset", async (req, res) => {
	const body = z.object({
		username: z.string(),
		code: z.string(),
		password: z.string(),
	}).parse(req.body);

	await pool.transaction(async (tx) => {
		const reset = await tx.maybeOne(sql.type(z.object({ user_id: z.string() }))`
			DELETE FROM werechat.password_reset
			WHERE code = ${body.code} AND user_id = ${body.username}
			RETURNING *
		`);

		if (reset === null) {
			res.status(403).send("Invalid reset code");
			return;
		}

		const passwordHash = await bcrypt.hash(body.password, 12);

		await pool.query(sql.unsafe`
			UPDATE werechat.user
			SET password = ${passwordHash}
			WHERE id = ${reset.user_id}
		`);

		res.json({ success: true });
	});
});

apiRouter.post("/session", (req, res) => {
	const session = new ChatSession();
	sessions.set(session.id, session);

	session.on("message", async (message) => {
		if (!session.authenticated) {
			return;
		}

		try {
			switch (message.kind) {
				case "Message": {
					const usersInRoom = await pool.anyFirst(sql.type(z.object({ user_id: z.string() }))`
						SELECT user_id
						FROM werechat.room_user
						WHERE room_id = ${message.room}
					`);

					if (!usersInRoom.includes(session.user)) {
						return;
					}

					logger.info({ room: message.room, user: session.user, message: message.content }, "Received message");

					const now = new Date();

					await pool.query(sql.unsafe`
						INSERT INTO werechat.message (room_id, user_id, content, timestamp)
						VALUES (${message.room}, ${session.user}, ${message.content}, ${now.toISOString()})
					`);

					for (const sess of sessions.values()) {
						if (sess.authenticated && usersInRoom.includes(sess.user)) {
							sess.send({
								kind: "Message",
								room: message.room,
								sender: session.user,
								content: message.content,
								timestamp: now.getTime()
							});
						}
					}
					break;
				}

				case "CreateRoom": {
					const room = await pool.transaction(async (tx) => {
						const room = await tx.one(sql.unsafe`
							INSERT INTO werechat.room (id, name)
							VALUES (${base64id()}, ${message.name})
							RETURNING *
						`);

						await tx.query(sql.unsafe`
							INSERT INTO werechat.room_user (room_id, user_id)
							VALUES (${room.id}, ${session.user})
						`);

						return room;
					});

					session.send({ kind: "RoomCreated", id: room.id, name: room.name, users: [session.user] });
					break;
				}

				case "LeaveRoom": {
					await pool.transaction(async (tx) => {
						const usersInRoom = await tx.anyFirst(sql.type(z.object({ user_id: z.string() }))`
							SELECT user_id
							FROM werechat.room_user
							WHERE room_id = ${message.room}
						`);

						if (!usersInRoom.includes(session.user)) {
							return;
						}

						await tx.query(sql.unsafe`
							DELETE FROM werechat.room_user
							WHERE room_id = ${message.room} AND user_id = ${session.user}
							RETURNING *
						`);

						session.send({ kind: "RoomLeft", room: message.room });
						for (const sess of sessions.values()) {
							if (sess.authenticated && usersInRoom.includes(sess.user) && sess.user !== session.user) {
								sess.send({ kind: "UserLeftRoom", room: message.room, user: session.user });
							}
						}
					});
					break;
				}

				case "AddToRoom": {
					await pool.transaction(async (tx) => {
						const room = await tx.maybeOne(sql.type(z.object({ id: z.string(), name: z.string() }))`
							SELECT room.*
							FROM werechat.room
								JOIN werechat.room_user ON room_user.room_id = room.id
							WHERE room.id = ${message.room} AND room_user.user_id = ${session.user}
						`);

						if (room === null) {
							return;
						}

						const usersInRoom = await tx.anyFirst(sql.type(z.object({ user_id: z.string() }))`
							SELECT user_id
							FROM werechat.room_user
							WHERE room_id = ${message.room}
						`);

						if (usersInRoom.includes(message.user)) {
							return;
						}

						await tx.query(sql.unsafe`
							INSERT INTO werechat.room_user (room_id, user_id)
							VALUES (${message.room}, ${message.user})
						`);

						for (const sess of sessions.values()) {
							if (sess.authenticated && usersInRoom.includes(sess.user)) {
								sess.send({ kind: "UserJoinedRoom", room: message.room, user: message.user });
							}

							if (sess.authenticated && sess.user === message.user) {
								sess.send({ kind: "RoomJoined", room: { id: room.id, name: room.name }, users: [...usersInRoom, sess.user] });
							}
						}
					});
				}
			}
		} catch (err) {
			console.error(err);
			logger.error({ err }, "Error processing message");
		}
	});

	session.on("end", () => {
		sessions.delete(session.id);
	});

	res.json({ id: session.id });
});

apiRouter.post("/session/:id/extend", (req, res) => {
	const session = sessions.get(req.params.id);

	if (session === undefined) {
		res.status(404).send("Session not found");
		return;
	}

	session.extend();
	res.json({ success: true });
});

apiRouter.delete("/session/:id", (req, res) => {
	const session = sessions.get(req.params.id);

	if (session === undefined) {
		res.status(404).send("Session not found");
		return;
	}

	if (session.authenticated && session.user !== req.werechat.user?.id) {
		res.status(403).send("Not authorized");
		return;
	}

	session.end();
	res.json({ success: true });
});

apiRouter.get("/self", async (req, res) => {
	if (req.werechat.user === undefined) {
		res.status(403).send("Not authenticated");
		return;
	}

	res.json({
		id: req.werechat.user.id,
		settings: req.werechat.user.settings,
	});
});

apiRouter.post("/settings", async (req, res) => {
	if (req.werechat.user === undefined) {
		res.status(403).send("Not authenticated");
		return;
	}

	const body = z.object({
		settings: z.object({
			fullMoonAction: z.discriminatedUnion("kind", [
				z.object({
					kind: z.literal("Block")
				}),
				z.object({
					kind: z.literal("Redirect"),
					url: z.string()
				}),
				z.object({
					kind: z.literal("Distract")
				})
			])
		})
	}).parse(req.body);

	await pool.query(sql.unsafe`
		UPDATE werechat.user
		SET settings = ${JSON.stringify(req.body.settings)}
		WHERE id = ${req.werechat.user.id}
	`);

	res.json({ success: true });
});

apiRouter.get("/rooms", async (req, res) => {
	if (req.werechat.user === undefined) {
		res.status(403).send("Not authenticated");
		return;
	}

	const rooms = await pool.any(sql.type(z.object({ id: z.string(), name: z.string(), users: z.array(z.string()) }))`
		WITH visible_rooms AS (
			SELECT room.*
			FROM werechat.room
				JOIN werechat.room_user ON room_user.room_id = room.id
			WHERE room_user.user_id = ${req.werechat.user.id}
		)
		SELECT visible_room.*, array_agg(room_user.user_id) AS users
		FROM visible_rooms visible_room
			JOIN werechat.room_user ON room_user.room_id = visible_room.id
		GROUP BY visible_room.id, visible_room.name
	`);

	res.json(rooms);
});

apiRouter.post("/room", async (req, res) => {
	if (req.werechat.user === undefined) {
		res.status(403).send("Not authenticated");
		return;
	}

	const body = z.object({
		name: z.string(),
	}).parse(req.body);

	const room = await pool.one(sql.type(z.object({ id: z.string(), name: z.string() }))`
		INSERT INTO werechat.room (name)
		VALUES (${base64id()}, ${body.name})
		RETURNING *
	`);

	await pool.query(sql.unsafe`
		INSERT INTO werechat.room_user (room_id, user_id)
		VALUES (${room.id}, ${req.werechat.user.id})
	`);

	res.json(room);
});

apiRouter.get("/room/:id/history", async (req, res) => {
	if (req.werechat.user === undefined) {
		res.status(403).send("Not authenticated");
		return;
	}

	const room = await pool.one(sql.type(z.object({ id: z.string(), name: z.string() }))`
		SELECT *
		FROM werechat.room
			JOIN werechat.room_user ON werechat.room_user.room_id = werechat.room.id
		WHERE werechat.room_user.user_id = ${req.werechat.user.id} AND werechat.room.id = ${req.params.id}
	`);

	const messages = await pool.any(sql.type(z.object({ content: z.string(), user_id: z.string(), timestamp: z.number() }))`
		SELECT *
		FROM werechat.message
		WHERE room_id = ${room.id}
		ORDER BY timestamp
	`);

	res.json({
		messages: messages.map((message) => ({
			content: message.content,
			from: message.user_id,
			timestamp: message.timestamp,
		})),
	});
});

apiRouter.ws("/ws", async (ws, req) => {
	if (typeof req.query.session !== "string") {
		ws.close();
		return;
	}

	const session = sessions.get(req.query.session);

	if (session === undefined) {
		ws.close(4000);
		return;
	}

	if (req.werechat.user === undefined) {
		ws.close(4000);
		return;
	}

	if (!session.authenticated) {
		session.authenticate(req.werechat.user.id);
	}

	try {
		const socket = new Socket(ws, InboundMessageSchema);
		socket.on("error", () => {
			logger.error("Socket error");
		})
		session.accept(socket);
	} catch (err) {
		ws.close(4000);
	}
});
