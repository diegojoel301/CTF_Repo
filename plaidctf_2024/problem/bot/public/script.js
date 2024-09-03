document.addEventListener("DOMContentLoaded", () => {
	const form = document.querySelector("form");
	const input = document.querySelector("input");

	form.addEventListener("submit", async (e) => {
		e.preventDefault();

		const response = await fetch("/visit", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ url: input.value })
		});

		if (response.ok) {
			document.querySelector(".result").textContent = "The bot will visit the URL shortly!";
		} else if (response.status === 429) {
			document.querySelector(".result").textContent = "The bot is still visiting the previous URL; please wait.";
		} else {
			document.querySelector(".result").textContent = "An error occurred.";
		}
	});
});