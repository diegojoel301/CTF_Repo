import EventEmitter from "node:events";
import { z } from "zod";

import base64id from "./base64id.js";
import { Session } from "./infra.js";
import { logger } from "./logger.js";

export const InboundMessageSchema = z.union([
	z.object({
		kind: z.literal("CreateRoom"),
		name: z.string(),
	}),
	z.object({
		kind: z.literal("AddToRoom"),
		room: z.string(),
		user: z.string(),
	}),
	z.object({
		kind: z.literal("Message"),
		room: z.string(),
		content: z.string(),
	}),
	z.object({
		kind: z.literal("LeaveRoom"),
		room: z.string(),
	}),
]);
type InboundMessage = z.infer<typeof InboundMessageSchema>;

const OutboundMessageSchema = z.union([
	z.object({
		kind: z.literal("Authenticated"),
		user: z.string(),
	}),
	z.object({
		kind: z.literal("RoomJoined"),
		room: z.object({
			id: z.string(),
			name: z.string(),
		}),
		users: z.array(z.string()),
	}),
	z.object({
		kind: z.literal("RoomCreated"),
		id: z.string(),
		name: z.string(),
		users: z.array(z.string()),
	}),
	z.object({
		kind: z.literal("Message"),
		room: z.string(),
		sender: z.string(),
		content: z.string(),
		timestamp: z.number(),
	}),
	z.object({
		kind: z.literal("RoomLeft"),
		room: z.string(),
	}),
	z.object({
		kind: z.literal("UserJoinedRoom"),
		room: z.string(),
		user: z.string(),
	}),
	z.object({
		kind: z.literal("UserLeftRoom"),
		room: z.string(),
		user: z.string(),
	})
]);
type OutboundMessage = z.infer<typeof OutboundMessageSchema>;

type ChatSessionState =
	| { kind: "Unauthed" }
	| { kind: "Authed"; user: string }
	;

export class ChatSession extends Session<InboundMessage, OutboundMessage> {
	#state: ChatSessionState;
	#rooms: Set<Room>;

	public constructor() {
		super();
		logger.info({ id: this.id }, "Session created");
		this.#state = { kind: "Unauthed" };
		this.#rooms = new Set();

		this.on("end", () => {
			logger.info({ id: this.id }, "Session ended");
		});
	}

	public authenticate(user: string): void {
		switch (this.#state.kind) {
			case "Unauthed": {
				this.#state = { kind: "Authed", user };
				logger.info({ id: this.id, user }, "Session authenticated");
				break;
			}

			case "Authed": {
				throw new Error("Session already authenticated");
			}
		}
	}

	public get authenticated(): boolean {
		return this.#state.kind === "Authed";
	}

	public get user(): string {
		if (this.#state.kind === "Authed") {
			return this.#state.user;
		} else {
			throw new Error("Session not authenticated");
		}
	}
}

interface RoomEvents {
	join: [ChatSession];
	leave: [ChatSession];
	message: [ChatSession, unknown];
}

export class Room extends EventEmitter<RoomEvents> {
	#id: string;
	#activeSessions: Map<string, ChatSession>;

	public constructor() {
		super();
		this.#id = base64id();
		this.#activeSessions = new Map();
	}

	public join(session: ChatSession) {
		this.#activeSessions.set(session.id, session);
		this.emit("join", session);
		session.on("end", () => {
			this.#activeSessions.delete(session.id);
			this.emit("leave", session);
		});
	}

	public send(sender: ChatSession, message: unknown): void {
		this.emit("message", sender, message);
	}

	public get id(): string {
		return this.#id;
	}
}