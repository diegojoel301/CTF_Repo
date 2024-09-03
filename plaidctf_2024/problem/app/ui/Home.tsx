import React from "react";

import { Layout } from "./Layout";
import { Nav } from "./Nav";
import { classes } from "./utils";

import ConfidenceImage from "./assets/confidence.png";
import FullMoonImage from "./assets/fullmoon.png";

import styles from "./Home.module.scss";

export const Home = () => (
	<Layout
		header={<Nav />}
	>
		<div className={styles.home}>
			<div className={styles.title}>Welcome to Werechat</div>
			<div className={styles.description}>
				Are you a lycanthrope who's tired of sending embarrassing messages to your friends while you're under the thrall of the full moon? Look no further! Werechat is the perfect solution for you. With our patented moon phase detection technology, we can ensure that your messages are only sent when you're in full control of your faculties.  Join a community of werewolves, werebears, and other werecreatures today!
			</div>
			<div className={classes(styles.section, styles.light)}>
				<div className={styles.sectionImage}>
					<img src={ConfidenceImage} width="400" alt="Werechat provides confidence" />
				</div>
				<div className={styles.sectionDescription}>
					<div className={styles.header}>Chat with Confidence</div>
					<div className={styles.content}>Send messages to your friends and family without worrying about embarrassing typos or messages sent in the heat of the moment.</div>
				</div>
			</div>
			<div className={styles.section}>
				<div className={styles.sectionDescription}>
					<div className={styles.header}>Be Safe During the Full Moon</div>
					<div className={styles.content}>Our moon phase detection technology ensures that your messages are only sent when you're in full control of your faculties.  We can also redirect or distract your were-form to prevent any incidents.</div>
				</div>
				<div className={styles.sectionImage}>
					<img src={FullMoonImage} width="400" alt="The full moon isn't so scary" />
				</div>
			</div>
		</div>
	</Layout>
);
