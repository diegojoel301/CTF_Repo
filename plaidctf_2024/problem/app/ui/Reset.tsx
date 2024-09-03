import React from "react";
import { Navigate } from "react-router-dom";

import { Layout } from "./Layout";
import { Nav } from "./Nav";
import { useSelf } from "./useSelf";
import { api, classes } from "./utils";

import styles from "./Reset.module.scss";

interface Props {
	className?: string;
}

export const Reset = (props: Props) => {
	const { self } = useSelf();
	const [username, setUsername] = React.useState<string>("");
	const [loading, setLoading] = React.useState<boolean>(false);
	const [requested, setRequested] = React.useState<boolean>(false);

	if (self !== undefined) {
		return <Navigate to="/chat" />;
	}

	const submit = async () => {
		setLoading(true);
		setRequested(false);
		try {
			const response = await api<{ success: boolean }>("POST", "request-reset", { username });
			if (response.success) {
				setRequested(true);
				setLoading(false);
			}
		} catch (e) {
			setLoading(false);
		}
	};

	return (
		<Layout className={styles.reset} header={<Nav />}>
			<div className={styles.resetContainer}>
				<form
					className={styles.resetForm}
					onSubmit={(e) => {
						e.preventDefault();
						submit();
					}}
				>
					<div className={styles.title}>Password Reset</div>
					<input
						className={classes(styles.input, styles.username)}
						type="text"
						name="username"
						placeholder="Username"
						value={username}
						onChange={(e) => setUsername(e.target.value)}
					/>
					<button
						className={styles.submit}
						disabled={loading}
					>
						Request Reset
					</button>
					{
						requested
							? (
								<div className={styles.requested}>
									Reset requested! Check your email.
								</div>
							)
							: null
					}
				</form>
			</div>
		</Layout>
	);
};
