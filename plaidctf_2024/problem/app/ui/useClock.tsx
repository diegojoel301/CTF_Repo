import { DateTime } from "luxon";
import React from "react";

import { useSelf } from "./useSelf";

const ClockContext = React.createContext<DateTime | undefined>(undefined);

interface ClockProviderProps {
	children: React.ReactNode;
}

export const ClockProvider = (props: ClockProviderProps) => {
	const userInfo = useSelf();
	const timezone = userInfo.self?.settings?.timezone;
	const [now, setNow] = React.useState(DateTime.now().setZone(timezone ?? "local"));

	React.useEffect(() => {
		const interval = setInterval(() => {
			setNow(DateTime.now().setZone(timezone ?? "local"));
		}, 1000);

		return () => clearInterval(interval);
	}, [timezone]);

	return (
		<ClockContext.Provider value={now}>
			{props.children}
		</ClockContext.Provider>
	);
};

export const useClock = () => {
	const now = React.useContext(ClockContext);

	if (now === undefined) {
		throw new Error("useClock must be used within a ClockProvider");
	}

	return now;
};
