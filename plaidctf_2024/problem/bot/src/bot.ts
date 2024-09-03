import * as puppeteer from "puppeteer";
import crypto from "node:crypto";
import pg from "pg";
import bcrypt from "bcrypt";
import { env } from "./env.js";

const flag = env.FLAG;
const appBase = `https://${env.APP_HOST}`;

export async function visit(url: string) {
	const db = new pg.Client(env.POSTGRES_URL);
	await db.connect();

	const username = crypto.randomBytes(16).toString("hex");
	const password = crypto.randomBytes(32).toString("hex");
	const email = crypto.randomBytes(16).toString("hex");
	const passwordHash = await bcrypt.hash(password, 12);
	console.log(`Creating user ${username} with password ${password}`);
	await db.query("INSERT INTO werechat.user (id, email, password) VALUES ($1, $2, $3)", [username, email, passwordHash]);
	await db.end();

	let browser: puppeteer.Browser | undefined;

	try {
		browser = await puppeteer.launch({
			headless: true,
			args: [
				"--no-sandbox",
				"--disable-setuid-sandbox",
				"--js-flags=--noexpose_wasm,--jitless"
			],
			env: {
				LD_PRELOAD: "/usr/local/lib/libfaketime.so.1",
				FAKETIME: "@2024-04-14 01:00:00"
			}
		});

		// Log in
		const page = await browser.newPage();
		await installSimulatedLocation(page);
		console.log("Logging in");
		await page.goto(appBase);
		await page.click("a[href='/login']");
		await page.waitForSelector("input[name=username]");
		await page.type("input[name=username]", username);
		await page.type("input[name=password]", password);
		await page.click("button");
		// Give it a couple of seconds to load
		await new Promise((resolve) => setTimeout(resolve, 2000));

		// Create chat
		console.log("Creating room");
		await page.waitForSelector("#create-room");
		await page.click("#create-room");
		await page.waitForSelector("input#name");
		await page.type("input#name", "Party Zone");
		await page.click("button[type=submit]");
		await page.waitForSelector("input[name=message]");
		await page.click("input[name=message]");
		await page.type("input[name=message]", "Hello, world!");
		await page.keyboard.press("Enter");

		// Set the flag cookie
		console.log("Setting flag cookie");
		await page.setCookie({ name: "FLAG", value: flag, domain: appBase.split("//")[1], path: "/" });

		// Close that page
		console.log("Closing page");
		await page.close();

		// Visit the target page
		console.log(`Visiting ${url}`);
		const targetPage = await browser.newPage();
		await new Promise((resolve) => setTimeout(resolve, 5000));
		await installSimulatedLocation(targetPage);
		await targetPage.goto(url, { timeout: 5000, waitUntil: "domcontentloaded" });
		await new Promise((resolve) => setTimeout(resolve, 120000));
	} catch (error) {
		console.error(error);
	} finally {
		if (browser !== undefined) {
			await browser.close();
		}
	}
}

async function installSimulatedLocation(page: puppeteer.Page) {
	// The location is always 40.30382, -80.43349
	// The time is always 2024-04-14 19:00 EDT (see FAKETIME above)
	await page.emulateTimezone("America/New_York");
	page.evaluateOnNewDocument(`
		navigator.geolocation.getCurrentPosition = (success) => {
			setTimeout(() => {
				success({ coords: { latitude: 40.30382, longitude: -80.43349 } });
			}, 2000);
		};
	`);
}
