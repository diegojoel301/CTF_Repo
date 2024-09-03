import React from "react";

import { FullMoonAction, useSelf } from "./useSelf";
import { useSession } from "./useSession";
import { api, classes } from "./utils";

import styles from "./Settings.module.scss";

interface Props {
	className?: string;
}

export const Settings = (props: Props) => {
	const { self, refresh } = useSelf();
	const [session, resetSession] = useSession();
	const dialogRef = React.useRef<HTMLDialogElement>(null);
	const [fullMoonAction, setFullMoonAction] = React.useState<FullMoonAction>({ kind: "Block" });
	const [timezone, setTimezone] = React.useState<string>("");

	React.useEffect(() => {
		if (dialogRef.current !== null) {
			dialogRef.current.showModal();
		}
	}, []);

	React.useEffect(() => {
		if (self !== undefined) {
			setTimezone(self.settings?.timezone ?? "local");
			setFullMoonAction(self.settings?.fullMoonAction ?? { kind: "Block" });
		}
	}, [self]);

	return (
		<dialog
			ref={dialogRef}
			className={classes(styles.settings, props.className)}
		>
			<form className={styles.form}>
				<div className={styles.title}>
					Settings
				</div>
				<div className={styles.field}>
					<label className={styles.label} htmlFor="timezone">Timezone</label>
					<select className={styles.input} value={timezone} onChange={(e) => setTimezone(e.target.value)}>
						<option value="local">Detect from Browser</option>
						<option value="utc">UTC</option>
						{Intl.supportedValuesOf("timeZone").map((tz) => (
							<option key={tz} value={tz}>{tz}</option>
						))}
					</select>
				</div>
				<div className={styles.field}>
					<label className={styles.label} htmlFor="fullMoonAction">When it's a full moon...</label>
					<div className={styles.radioOptions}>
						<div className={styles.radioOption}>
							<input
								type="radio"
								id="block"
								className={styles.radioButton}
								name="fullMoonAction"
								value="block"
								checked={fullMoonAction.kind === "Block"}
								onChange={() => setFullMoonAction({ kind: "Block" })}
							/>
							<label className={styles.radioLabel} htmlFor="block">Block access to chat</label>
						</div>
						<div className={styles.radioOption}>
							<input
								type="radio"
								id="redirect"
								className={styles.radioButton}
								name="fullMoonAction"
								value="redirect"
								checked={fullMoonAction.kind === "Redirect"}
								onChange={() => setFullMoonAction({ kind: "Redirect", url: "" })}
							/>
							<label className={styles.radioLabel} htmlFor="redirect">Redirect me to...</label>
							<input
								className={styles.input}
								type="text"
								value={fullMoonAction.kind === "Redirect" ? fullMoonAction.url : ""}
								onChange={(e) => setFullMoonAction({ kind: "Redirect", url: e.target.value })}
								placeholder="URL"
								disabled={fullMoonAction.kind !== "Redirect"}
							/>
						</div>
						<div className={styles.radioOption}>
							<input
								type="radio"
								id="distract"
								className={styles.radioButton}
								name="fullMoonAction"
								value="distract"
								checked={fullMoonAction.kind === "Distract"}
								onChange={() => setFullMoonAction({ kind: "Distract" })}
							/>
							<label className={styles.radioLabel} htmlFor="distract">Distract me</label>
						</div>
					</div>
				</div>
				<div className={styles.buttons}>
					<button
						type="button"
						className={classes(styles.button, styles.primary)}
						onClick={async () => {
							await api("POST", "settings", {
								settings: {
									fullMoonAction,
									timezone,
								},
							});
							refresh();
							resetSession();
						}}
					>
						Save
					</button>
				</div>
			</form>
		</dialog>
	);
};