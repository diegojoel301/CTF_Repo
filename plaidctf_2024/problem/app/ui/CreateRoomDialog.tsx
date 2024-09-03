import React from "react";

import styles from "./CreateRoomDialog.module.scss";
import { classes } from "./utils";

interface Props {
	onClose: () => void;
	onCreateRoom: (name: string) => void;
}

export const CreateRoomDialog = (props: Props) => {
	const dialogRef = React.useRef<HTMLDialogElement>(null);
	const [name, setName] = React.useState<string>("");

	React.useEffect(() => {
		if (dialogRef.current !== null) {
			dialogRef.current.showModal();
		}
	}, []);

	return (
		<dialog ref={dialogRef} className={styles.createRoomDialog}>
			<form
				className={styles.form}
				onSubmit={(e) => {
					e.preventDefault();
					props.onCreateRoom(name);
				}}
			>
				<div className={styles.title}>
					Create Room
				</div>
				<div className={styles.field}>
					<label className={styles.label} htmlFor="name">Name</label>
					<input className={styles.input} type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} />
				</div>
				<div className={styles.buttons}>
					<button className={classes(styles.button, styles.secondary)} type="button" onClick={props.onClose}>Cancel</button>
					<button className={classes(styles.button, styles.primary)} type="submit" disabled={name === ""}>Create</button>
				</div>
			</form>
		</dialog>
	);
};