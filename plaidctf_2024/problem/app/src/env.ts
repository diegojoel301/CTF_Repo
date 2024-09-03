import { z } from "zod";

export const env = z.object({
	POSTGRES_URL: z.string(),
	SENDGRID_API_KEY: z.string().optional(),
}).parse(process.env);
