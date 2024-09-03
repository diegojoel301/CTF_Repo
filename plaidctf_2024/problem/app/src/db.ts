import { createPool } from "slonik";

import { env } from "./env.js";
import { createResultParserInterceptor } from "./zodInterceptor.js";

export const pool = await createPool(env.POSTGRES_URL, {
	interceptors: [
		createResultParserInterceptor()
	]
});
