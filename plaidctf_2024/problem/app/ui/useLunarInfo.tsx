import { createMoon } from "astronomy-bundle/moon";
import { createSun } from "astronomy-bundle/sun";
import { createTimeOfInterest } from "astronomy-bundle/time";
import { DateTime } from "luxon";
import React from "react";

import { useClock } from "./useClock";
import { useLocation } from "./useLocation";

export interface LunarInfo {
	illuminated: number;
	waxing: boolean;
	sunset: DateTime;
	sunrise: DateTime;
}

const LunarInfoContext = React.createContext<LunarInfo | undefined | null>(null);

interface LunarInfoProviderProps {
	children: React.ReactNode;
}

export const LunarInfoProvider = (props: LunarInfoProviderProps) => {
	const [lunarInfo, setLunarInfo] = React.useState<LunarInfo | undefined>(undefined);
	const { location } = useLocation();
	// const location = { latitude: 0, longitude: 0 };
	const clock = useClock();

	const midnight = React.useMemo(() => (
		clock.hour < 12
			? clock.startOf("day")
			: clock.startOf("day").plus({ days: 1 })
	), [clock]);

	const [prevNoonToi, midnightToi, nextNoonToi] = React.useMemo(() => {
		const yesterday = midnight.minus({ days: 1 });
		return [
			createTimeOfInterest.fromTime(yesterday.year, yesterday.month, yesterday.day, 12, 0, 0),
			createTimeOfInterest.fromTime(midnight.year, midnight.month, midnight.day, 0, 0, 0),
			createTimeOfInterest.fromTime(midnight.year, midnight.month, midnight.day, 12, 0, 0),
		];
	}, [midnight.valueOf()]);

	React.useEffect(() => {
		if (location === undefined) {
			return;
		}

		setLunarInfo(undefined);
		(async () => {
			const sunPrevNoon = createSun(prevNoonToi);
			const moonMidnight = createMoon(midnightToi);
			const sunNextNoon = createSun(nextNoonToi);
			const [illuminated, waxing, sunset, sunrise] = await Promise.all([
				moonMidnight.getIlluminatedFraction(),
				moonMidnight.isWaxing(),
				sunPrevNoon.getSet({ lat: location.latitude, lon: location.longitude, elevation: 0 }),
				sunNextNoon.getRise({ lat: location.latitude, lon: location.longitude, elevation: 0 }),
			]);

			const sunsetTime = sunset.getTime();
			const sunriseTime = sunrise.getTime();

			const sunsetTimeShifted = DateTime.fromObject({
				hour: sunsetTime.hour,
				minute: sunsetTime.min,
				second: sunsetTime.sec,
			}, { zone: "utc" }).setZone(clock.zone);

			const sunriseTimeShifted = DateTime.fromObject({
				hour: sunriseTime.hour,
				minute: sunriseTime.min,
				second: sunriseTime.sec,
			}, { zone: "utc" }).setZone(clock.zone);

			const sunsetDateTime = midnight.minus({ days: 1 }).set({ hour: sunsetTimeShifted.hour, minute: sunsetTimeShifted.minute, second: sunsetTimeShifted.second });
			const sunriseDateTime = midnight.set({ hour: sunriseTimeShifted.hour, minute: sunriseTimeShifted.minute, second: sunriseTimeShifted.second });

			setLunarInfo({
				illuminated,
				waxing,
				sunset: sunsetDateTime,
				sunrise: sunriseDateTime,
			});
		})();
	}, [location, midnight.valueOf(), prevNoonToi.T, midnightToi.T, nextNoonToi.T]);

	return (
		<LunarInfoContext.Provider value={lunarInfo}>
			{props.children}
		</LunarInfoContext.Provider>
	);
};

export const useLunarInfo = () => {
	const lunarInfo = React.useContext(LunarInfoContext);

	if (lunarInfo === null) {
		throw new Error("useLunarInfo must be used within a LunarInfoProvider");
	}

	return lunarInfo;
};
