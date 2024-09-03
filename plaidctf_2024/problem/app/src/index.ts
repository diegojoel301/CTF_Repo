import cookieParser from "cookie-parser";
import express from "express";
import "express-async-errors";
import expressWs from "express-ws";
import { readFile } from "node:fs/promises";
import { ZodError } from "zod";

import base64id from "./base64id.js";
import { logger } from "./logger.js";

declare global {
	namespace Express {
		interface Request {
			werechat: {
				nonce?: string;
				user?: {
					id: string;
					settings?: unknown;
				};
			};
		}
	}
}

const indexHtml = (await readFile("dist-ui/index.html")).toString();

const { app } = expressWs(express());

app.set("views", "views");

app.use(express.json({ type: "*/*" }));
app.use(cookieParser());

app.use("/api", (await import("./api.js")).apiRouter);

app.use(async (req, res, next) => {
	logger.debug({ method: req.method, path: req.path, ip: req.ip }, "Received request");

	req.werechat = { nonce: base64id() };
	res.header("Content-Security-Policy", `
		default-src 'self';
		script-src 'nonce-${req.werechat.nonce}';
		style-src-elem 'nonce-${req.werechat.nonce}';
		font-src 'self' fonts.gstatic.com;
		img-src 'self';
		frame-src www.youtube.com
	`.replace(/[\n\s]+/g, " "));
	res.header("X-Content-Type-Options", "nosniff");
	res.header("X-Frame-Options", "DENY");

	next();
});

app.use("/assets", express.static("dist-ui/assets", { maxAge: "1y" }));
app.use((req, res, next) => {
	if (req.path.startsWith("/api")) {
		return next();
	}

	return res.send(indexHtml.replace(/NONCEPLACEHOLDER/g, req.werechat.nonce!));
});

app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
	logger.error(err);
	if (err instanceof ZodError) {
		res.status(400).json(err.errors);
	} else {
		res.status(500).send("Internal server error");
	}
});

app.listen(80, () => {
	console.log("Listening on port 80");
});
