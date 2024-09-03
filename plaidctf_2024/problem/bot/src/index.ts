import express from "express";
import { visit } from "./bot.js";
import { z, ZodError } from "zod";

const app = express();
app.use(express.json());

let visiting = false;

app.post("/visit", async (req, res) => {
	const body = z.object({
		url: z.string().refine((url) => url.startsWith("http://") || url.startsWith("https://"), {
			message: "URL must start with http:// or https://"
		})
	}).parse(req.body);

	if (visiting) {
		res.status(429).send("Already visiting");
		return;
	}

	visiting = true;

	try {
		res.json({ success: true });
		await visit(body.url);
	} catch (e) {
		console.error(e);
	} finally {
		visiting = false;
	}
});

app.use(express.static("public"));

app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
	console.error(err);
	if (err instanceof ZodError) {
		res.status(400).json(err.errors);
	} else {
		res.status(500).send("Internal server error");
	}
});

app.listen(80, () => {
	console.log("Listening on port 80");
});