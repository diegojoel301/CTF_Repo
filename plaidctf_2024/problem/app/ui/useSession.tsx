import React from "react";

import { api } from "./utils";

interface SessionInfo {
	session?: string;
	resetSession: () => void;
	consumeSession: (() => void);
}

const SessionContext = React.createContext<SessionInfo | undefined>(undefined);

interface SessionProviderProps {
	children: React.ReactNode;
	loadingContent?: React.ReactNode;
}

export const SessionProvider = (props: SessionProviderProps) => {
	const [needsSession, setNeedsSession] = React.useState(true);
	const [session, setSession] = React.useState<string | undefined>(undefined);
	const [extendInterval, setExtendInterval] = React.useState<ReturnType<typeof setInterval> | undefined>(undefined);
	const [extendCount, setExtendCount] = React.useState(0);

	React.useEffect(() => {
		if (needsSession) {
			setNeedsSession(false);
			api<{ id: string }>("POST", "session")
				.then(({ id }) => {
					setSession(id);
					setExtendCount(0);
					setExtendInterval(
						setInterval(() => {
							api("POST", `session/${id}/extend`);
							setExtendCount((count) => count + 1);
						}, 5000)
					);
				});
		}
	}, [needsSession]);

	React.useEffect(() => {
		if (extendCount > 3) {
			api("DELETE", `session/${session}`);
			setSession(undefined);
			setExtendCount(0);
			clearInterval(extendInterval);
			setExtendInterval(undefined);
		}
	}, [extendCount, extendInterval]);

	const resetSession = React.useCallback(() => {
		setSession(undefined);
		setExtendCount(0);
		clearInterval(extendInterval);
		setNeedsSession(true);
	}, []);

	const consumeSession = React.useCallback(() => {
		if (session !== undefined) {
			clearInterval(extendInterval);
		} else {
			resetSession();
		}
	}, [session, resetSession]);

	return (
		<SessionContext.Provider
			value={{
				session,
				resetSession,
				consumeSession
			}}
		>
			{props.children}
		</SessionContext.Provider>
	);
}

export const useSession = () => {
	const sessionInfo = React.useContext(SessionContext);

	if (sessionInfo === undefined) {
		throw new Error("useSession must be used within a SessionProvider");
	}

	React.useEffect(() => {
		sessionInfo.consumeSession();
	}, [sessionInfo.session]);

	return [sessionInfo.session, sessionInfo.resetSession] as const;
};
