import React from "react";
import { Navigate } from "react-router-dom";

import styles from "./FullMoonGate.module.scss";
import { Layout } from "./Layout";
import { Loader } from "./Loader";
import { useClock } from "./useClock";
import { useLocation } from "./useLocation";
import { useLunarInfo } from "./useLunarInfo";
import { useSelf } from "./useSelf";

interface Props {
	children: React.ReactNode;
}

export const FullMoonGate = (props: Props) => {
	const { self, loading: selfLoading } = useSelf();
	const clock = useClock();
	const lunarInfo = useLunarInfo();
	const [activated, setActivated] = React.useState<boolean>(navigator.userActivation.hasBeenActive);
	const { declined } = useLocation();

	React.useEffect(() => {
		setActivated(navigator.userActivation.hasBeenActive);
	}, [selfLoading, lunarInfo === undefined]);

	React.useEffect(() => {
		if (
			lunarInfo !== undefined
			&& lunarInfo.sunset < clock
			&& clock < lunarInfo.sunrise
			&& lunarInfo.illuminated > 0.875
			&& self?.settings?.fullMoonAction?.kind === "Redirect"
		) {
			window.location.assign(self.settings.fullMoonAction.url);
		}
	}, [clock, lunarInfo]);

	if (declined) {
		return (
			<Layout className={styles.fullMoonGate}>
				<div className={styles.fullMoonGateContainer}>
					<div className={styles.error}>
						<div className={styles.headline}>
							You must enable location services to access this site.
						</div>
						<div className={styles.subhead}>
							Otherwise, we can't protect you from the full moon! <br />
							Please enable location access and refresh the page.
						</div>
					</div>
				</div>
			</Layout>
		)
	}

	if (selfLoading || lunarInfo === undefined) {
		return (
			<Layout className={styles.fullMoonGate}>
				<div className={styles.fullMoonGateContainer}>
					<div className={styles.loading}>
						Checking the moon phase... <Loader className={styles.loader} />
					</div>
				</div>
			</Layout>
		);
	}

	if (self === undefined) {
		return <Navigate to="/login" />;
	}

	if (
		lunarInfo.sunset < clock
		&& clock < lunarInfo.sunrise
		&& lunarInfo.illuminated > 0.875
	) {
		switch (self.settings?.fullMoonAction?.kind) {
			case "Distract": {
				return (
					<Layout>
						<div className={styles.distract}>
							<div className={styles.headline}>It is currently a full moon.</div>
							<div className={styles.subhead}>Please enjoy this engaging content until sunrise in {lunarInfo.sunrise.diff(clock).toFormat("hh:mm:ss")}.</div>
							<iframe
								className={styles.video}
								src={`https://www.youtube.com/embed/dip2w_rGzn0?si=EGhPK9yY_UNsn1Ec&controls=0&autoplay=1${activated ? "" : "&mute=1"}`}
								title="YouTube video player"
								frameBorder="0"
								allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
								allowFullScreen
							/>
						</div>
					</Layout>
				);
			}

			case "Redirect": {
				// fallthrough to default, redirect handled by useEffect
			}

			case undefined:
			case "Block": {
				return (
					<Layout>
						<div className={styles.block}>
							<div className={styles.headline}>It is currently a full moon.</div>
							<div className={styles.subhead}>Please return at sunrise in {lunarInfo.sunrise.diff(clock).toFormat("hh:mm:ss")}.</div>
						</div>
					</Layout>
				);
			}
		}
	} else {
		return props.children;
	}
};
