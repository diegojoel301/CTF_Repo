import React from "react";

import { useSession } from "./useSession";

export const useWebsocket = () => {
	const [session, resetSession] = useSession();
	const [ws, setWs] = React.useState<WebSocket | undefined>(undefined);
	const [connectTimeout, setConnectTimeout] = React.useState<number | undefined>(undefined);

	const attemptConnect = React.useCallback(() => {
		if (session === undefined) {
			return;
		}

		const ws = new WebSocket(`${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/api/ws?session=${session}`);
		const onEarlyClose = (event: CloseEvent) => {
			setWs(undefined);
			if (event.code === 4000) {
				resetSession();
			} else {
				setConnectTimeout(window.setTimeout(attemptConnect, 1000));
			}
		};
		const onFirstPingOrMessage = () => {
			ws.removeEventListener("close", onEarlyClose);
			ws.removeEventListener("ping", onFirstPingOrMessage);
			ws.removeEventListener("message", onFirstPingOrMessage);
			ws.addEventListener("close", () => {
				setWs(undefined);
				attemptConnect();
			});
		};
		ws.addEventListener("close", onEarlyClose);
		ws.addEventListener("ping", onFirstPingOrMessage);
		ws.addEventListener("message", onFirstPingOrMessage);
		ws.addEventListener("open", () => {
			setWs(ws);
		});
		window.addEventListener("keydown", (event) => {
			if (event.key === "Escape") {
				ws.close();
			}
		});
	}, [session]);

	React.useEffect(() => {
		attemptConnect();

		return () => {
			if (ws !== undefined) {
				ws.close();
			}
			if (connectTimeout !== undefined) {
				window.clearTimeout(connectTimeout);
			}
		};
	}, [session]);

	return ws;
};
