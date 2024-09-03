import React from "react";
import { NavLink } from "react-router-dom";

import { classes } from "./utils";

import styles from "./Nav.module.scss";

export const Nav = () => (
	<div className={styles.nav}>
		<NavLink
			to="/login"
			className={({ isActive }) => classes(styles.link, isActive ? styles.active : undefined)}
		>
			Log In
		</NavLink>
		<NavLink
			to="/register"
			className={({ isActive }) => classes(styles.link, isActive ? styles.active : undefined)}
		>
			Register
		</NavLink>
	</div>
)