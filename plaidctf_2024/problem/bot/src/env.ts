import { z } from "zod";

export const env = z.object({
	POSTGRES_URL: z.string(),
	APP_HOST: z.string(),
	FLAG: z.string().default("PCTF{fake_flag}")
}).parse(process.env);
