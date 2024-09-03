export function classes(...args: (string | undefined)[]): string {
	return args.filter((x) => x !== undefined).join(" ");
}

export async function api<T>(method: string, endpoint: string, body?: unknown): Promise<T> {
	let request: RequestInit = { method };

	if (body !== undefined) {
		request = {
			...request,
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(body),
		};
	}

	const response = await fetch(`/api/${endpoint}`, request);

	if (!response.ok) {
		throw new Error((await response.text()) || response.statusText);
	}

	return response.json() as T;
}
