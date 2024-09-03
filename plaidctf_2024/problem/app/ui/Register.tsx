import React from "react";
import { Navigate, useNavigate } from "react-router-dom";

import styles from "./Register.module.scss";
import { Layout } from "./Layout";
import { useSelf } from "./useSelf";
import { api, classes } from "./utils";
import { Nav } from "./Nav";

interface Props {
	className?: string;
}

export const Register = (props: Props) => {
	const { self, loading: selfLoading, refresh } = useSelf();
	const [inviteCode, setInviteCode] = React.useState<string>("");
	const [username, setUsername] = React.useState<string>("");
	const [email, setEmail] = React.useState<string>("");
	const [password, setPassword] = React.useState<string>("");
	const [loading, setLoading] = React.useState<boolean>(false);
	const navigate = useNavigate();

	if (self !== undefined) {
		return <Navigate to="/chat" />;
	}

	const submit = async () => {
		setLoading(true);
		try {
			await api("POST", "register", { inviteCode, username, email, password });
			navigate("/login");
		} catch (e) {
			setLoading(false);
		}
	};

	return (
		<Layout className={styles.register} header={<Nav />}>
			<div className={styles.registerContainer}>
				<form
					className={styles.registerForm}
					onSubmit={(e) => {
						e.preventDefault();
						submit();
					}}
				>
					<div className={styles.title}>Register</div>
					<input
						className={classes(styles.input, styles.inviteCode)}
						type="text"
						name="inviteCode"
						placeholder="Invite Code"
						value={inviteCode}
						onChange={(e) => setInviteCode(e.target.value)}
					/>
					<input
						className={classes(styles.input, styles.username)}
						type="text"
						name="username"
						placeholder="Username"
						value={username}
						onChange={(e) => setUsername(e.target.value)}
					/>
					<input
						className={classes(styles.input, styles.email)}
						type="email"
						name="email"
						placeholder="Email"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
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
						Register
					</button>
				</form>
			</div>
		</Layout>
	);
};
