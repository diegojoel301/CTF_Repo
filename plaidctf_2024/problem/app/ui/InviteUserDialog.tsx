import React from "react";

import { classes } from "./utils";

import styles from "./InviteUserDialog.module.scss";

interface Props {
	onClose: () => void;
	onInviteUser: (name: string) => void;
}

export const InviteUserDialog = (props: Props) => {
	const dialogRef = React.useRef<HTMLDialogElement>(null);
	const [name, setName] = React.useState<string>("");

	React.useEffect(() => {
		if (dialogRef.current !== null) {
			dialogRef.current.showModal();
		}
	}, []);

	return (
		<dialog ref={dialogRef} className={styles.inviteUserDialog}>
			<form
				className={styles.form}
				onSubmit={(e) => {
					e.preventDefault();
					props.onInviteUser(name);
				}}
			>
				<div className={styles.title}>
					Invite User
				</div>
				<div className={styles.field}>
					<label className={styles.label} htmlFor="name">Name</label>
					<input className={styles.input} type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} />
				</div>
				<div className={styles.buttons}>
					<button className={classes(styles.button, styles.secondary)} type="button" onClick={props.onClose}>Cancel</button>
					<button className={classes(styles.button, styles.primary)} type="submit">Invite</button>
				</div>
			</form>
		</dialog>
	);
};