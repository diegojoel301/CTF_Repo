import React from "react";
import { Link } from "react-router-dom";

import { useClock } from "./useClock";
import { useLocation } from "./useLocation";
import { useLunarInfo } from "./useLunarInfo";
import { classes } from "./utils";

import styles from "./Layout.module.scss";

interface Props {
	className?: string;
	sidebar?: React.ReactNode;
	header?: React.ReactNode;
	children: React.ReactNode;
}

const MoonEmoji = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘", "🌑"];
const SunEmoji = "☀️";

export const Layout = (props: Props) => {
	const clock = useClock();
	const { location } = useLocation();
	const lunarInfo = useLunarInfo();

	const emoji = React.useMemo(() => {
		if (lunarInfo === undefined || location === undefined) {
			return MoonEmoji[4];
		}

		if (clock < lunarInfo.sunset || clock > lunarInfo.sunrise) {
			return SunEmoji;
		}

		let index = Math.floor((lunarInfo.illuminated + 0.125) / 0.25);
		if (!lunarInfo.waxing) {
			index = 8 - index;
		}
		if (location.latitude < 0) {
			index = 8 - index;
		}
		return MoonEmoji[index];
	}, [lunarInfo, location]);

	React.useEffect(() => {
		document.getElementById("favicon")?.setAttribute(
			"href",
			`data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>${emoji}</text></svg>`
		);
	}, [emoji]);

	return (
		<div
			className={classes(
				styles.layout,
				props.sidebar !== undefined ? styles.withSidebar : undefined,
				props.className
			)}
		>
			<Link to="/" className={styles.title}>
				<div className={styles.emoji}>
					{emoji}
				</div>
				<div className={styles.werechat}>
					Werechat
				</div>
			</Link>
			<div className={styles.header}>
				{props.header}
			</div>
			<div className={styles.sidebar}>
				{props.sidebar}
			</div>
			<div className={styles.content}>
				{props.children}
			</div>
		</div>
	);
}