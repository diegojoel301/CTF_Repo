import React from "react";
import { Link, Navigate } from "react-router-dom";

import { Layout } from "./Layout";
import { Nav } from "./Nav";
import { useSelf } from "./useSelf";
import { api, classes } from "./utils";

import styles from "./Login.module.scss";

interface Props {
	className?: string;
}

export const Login = (props: Props) => {
	const { self, loading: selfLoading, refresh } = useSelf();
	const [username, setUsername] = React.useState<string>("");
	const [password, setPassword] = React.useState<string>("");
	const [loading, setLoading] = React.useState<boolean>(false);

	if (self !== undefined) {
		return <Navigate to="/chat" />;
	}

	const submit = async () => {
		setLoading(true);
		try {
			await api("POST", "login", { username, password });
			await refresh();
		} catch (e) {
			setLoading(false);
		}
	};

	return (
		<Layout className={styles.login} header={<Nav />}>
			<div className={styles.loginContainer}>
				<form
					className={styles.loginForm}
					onSubmit={(e) => {
						e.preventDefault();
						submit();
					}}
				>
					<div className={styles.title}>Log In</div>
					<input
						className={classes(styles.input, styles.username)}
						type="text"
						name="username"
						placeholder="Username"
						value={username}
						onChange={(e) => setUsername(e.target.value)}
					/>
					<input
						className={classes(styles.input, styles.password)}
						type="password"
						name="password"
						placeholder="Password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
					/>
					<button
						className={styles.submit}
						disabled={loading}
					>
						Login
					</button>
					<Link to="/reset" className={styles.reset}>
						Forgot password?
					</Link>
				</form>
			</div>
		</Layout>
	);
};
