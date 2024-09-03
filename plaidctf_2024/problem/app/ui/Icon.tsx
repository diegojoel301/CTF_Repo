import React from "react";

import { classes } from "./utils";

import styles from "./Icon.module.scss";

interface Props {
	className?: string;
	name: string;
}

export const Icon = (props: Props) => (
	<span className={classes(styles.icon, props.className)}>
		{props.name}
	</span>
);
