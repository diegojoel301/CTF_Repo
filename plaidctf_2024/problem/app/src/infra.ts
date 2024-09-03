import EventEmitter from "node:events";
import WebSocket from "ws";
import { ZodType, z } from "zod";

import base64id from "./base64id.js";
import { logger } from "./logger.js";

const PingInterval = 5000;
const SessionTimeout = 30000;
const DroppedPingLimit = 3;

interface SocketEvents<InboundMessage> {
	close: [];
	error: [];
	ping: [];
	pong: [];
	message: [InboundMessage];
	ack: [number];
}

export class Socket<InboundMessage, OutboundMessage> extends EventEmitter<SocketEvents<InboundMessage>> {
	private ws: WebSocket;
	private pingInterval: NodeJS.Timeout;
	private droppedPings: number;
	private messageSchema: ZodType<InboundMessage | { kind: "Ack"; seq: number }>;

	public constructor(
		ws: WebSocket,
		messageSchema: ZodType<InboundMessage>
	) {
		super();
		this.ws = ws;
		this.droppedPings = 0;
		this.messageSchema = z.union([
			messageSchema,
			z.object({
				kind: z.literal("Ack"),
				seq: z.number(),
			}),
		]);

		this.pingInterval = setInterval(() => {
			if (this.droppedPings >= DroppedPingLimit) {
				this.ws.terminate();
				this.emit("error");
				this.terminate();
				return;
			}
			this.emit("ping");
			this.ws.ping();
			this.droppedPings++;
		}, PingInterval);

		this.ws.on("pong", () => {
			this.emit("pong");
			this.droppedPings = 0;
		});

		this.ws.on("message", (data: string | Buffer | ArrayBuffer) => {
			try {
				let message: InboundMessage | { kind: "Ack"; seq: number };
				logger.trace({ data }, "Received unparsed message");

				if (typeof data === "string") {
					message = this.messageSchema.parse(JSON.parse(data));
				} else {
					message = this.messageSchema.parse(JSON.parse(data.toString()));
				}

				logger.trace({ message }, "Received message");

				if (typeof message === "object" && message !== null && "kind" in message && message.kind === "Ack") {
					this.emit("ack", message.seq);
				} else {
					this.emit("message", message as InboundMessage);
				}
			} catch (err) {
				logger.error({ err }, "Invalid message");
			}
		});

		this.ws.on("close", (code) => {
			logger.debug({ code }, "Socket closed");
			if (
				code === 1000 // Normal closure
				|| code === 1001 // Going away
				|| code === 1005 // No status
			) {
				this.emit("close");
			} else {
				this.emit("error");
			}
			this.terminate();
		});

		this.ws.on("error", (error) => {
			logger.debug({ error }, "Socket error");
			this.emit("error");
			this.terminate();
		});
	}

	public send(data: { seq: number, data: OutboundMessage }): void {
		this.ws.send(JSON.stringify(data));
	}

	public forceClose(): void {
		this.ws.terminate();
		this.terminate();
	}

	private terminate(): void {
		clearInterval(this.pingInterval);
	}
}

interface SessionEvents<InboundMessage> {
	message: [InboundMessage];
	connect: [];
	disconnect: [];
	reconnect: [];
	end: [];
}

type SessionState<InboundMessage, OutboundMessage> =
	| { kind: "BeforeConnect"; timeout: NodeJS.Timeout }
	| { kind: "Connected"; socket: Socket<InboundMessage, OutboundMessage> }
	| { kind: "Disconnected"; timeout: NodeJS.Timeout }
	| { kind: "Ended" }
	;

export class Session<InboundMessage, OutboundMessage> extends EventEmitter<SessionEvents<InboundMessage>> {
	#id: string;
	#state: SessionState<InboundMessage, OutboundMessage>;
	#messages: OutboundMessage[];
	#seq: number;

	public constructor() {
		super();
		this.#id = base64id();
		this.#state = { kind: "BeforeConnect", timeout: setTimeout(() => this.end(), SessionTimeout) };
		this.#messages = [];
		this.#seq = 0;
	}

	public extend(): void {
		if (this.#state.kind !== "BeforeConnect") {
			throw new Error("Session not in BeforeConnect state");
		}

		clearTimeout(this.#state.timeout);
		this.#state.timeout = setTimeout(() => this.end(), SessionTimeout);
	}

	public accept(socket: Socket<InboundMessage, OutboundMessage>): void {
		switch (this.#state.kind) {
			case "BeforeConnect": {
				clearTimeout(this.#state.timeout);
				this.#state = { kind: "Connected", socket };
				this.installHandlers(socket);
				this.emit("connect");
				break;
			}

			case "Connected": {
				throw new Error("Session already connected");
			}

			case "Disconnected": {
				clearTimeout(this.#state.timeout);
				this.#state = { kind: "Connected", socket };
				this.installHandlers(socket);
				this.emit("reconnect");
				for (let i = 0; i < this.#messages.length; i++) {
					this.#state.socket.send({ seq: this.#seq + i, data: this.#messages[i] });
				}
				break;
			}

			case "Ended": {
				throw new Error("Session already ended");
			}
		}
	}

	public get id(): string {
		return this.#id;
	}

	public send(data: OutboundMessage): void {
		switch (this.#state.kind) {
			case "BeforeConnect": {
				throw new Error("Session not connected");
			}

			case "Connected": {
				this.#messages.push(data);
				this.#state.socket.send({ seq: this.#seq + this.#messages.length, data });
				break;
			}

			case "Disconnected": {
				this.#messages.push(data);
				break;
			}

			case "Ended": {
				throw new Error("Session already ended");
			}
		}
	}

	private installHandlers(socket: Socket<InboundMessage, OutboundMessage>): void {
		socket.on("close", () => {
			logger.debug({ id: this.#id }, "Socket closed");
			this.end();
		});

		socket.on("error", () => {
			logger.debug({ id: this.#id }, "Socket error");
			this.disconnect();
		});

		socket.on("message", (message) => {
			this.emit("message", message);
		});

		socket.on("ack", (seq) => {
			const count = seq - this.#seq;
			this.#messages = this.#messages.slice(count);
			this.#seq = seq;
		});

		socket.on("ping", () => {
			logger.trace({ id: this.#id }, "Ping");
		});

		socket.on("pong", () => {
			logger.trace({ id: this.#id }, "Pong");
		});
	}

	private disconnect(): void {
		switch (this.#state.kind) {
			case "BeforeConnect": {
				throw new Error("Session not connected");
			}

			case "Connected": {
				this.#state.socket.removeAllListeners();
				this.#state = {
					kind: "Disconnected",
					timeout: setTimeout(() => this.end(), SessionTimeout)
				};
				this.emit("disconnect");
				break;
			}

			case "Disconnected":
			case "Ended": {
				throw new Error("Session already ended");
			}
		}
	}

	public end(): void {
		switch (this.#state.kind) {
			case "BeforeConnect": {
				clearTimeout(this.#state.timeout);
				this.#state = { kind: "Ended" };
				this.emit("end");
				break;
			}

			case "Connected": {
				this.#state.socket.forceClose();
				this.#state = { kind: "Ended" };
				this.emit("end");
				break;
			}

			case "Disconnected": {
				clearTimeout(this.#state.timeout);
				this.#state = { kind: "Ended" };
				this.emit("end");
				break;
			}

			case "Ended": {
				throw new Error("Session already ended");
			}
		}
	}
}
