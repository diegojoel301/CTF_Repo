import React from "react";

const MoonEmoji = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"];

interface Props {
	className?: string;
}

export const Loader = (props: Props) => {
	const [index, setIndex] = React.useState(0);

	React.useEffect(() => {
		const interval = setInterval(() => {
			setIndex((i) => (i + 1) % MoonEmoji.length);
		}, 80);
		return () => clearInterval(interval);
	}, []);

	return <span className={props.className}>{MoonEmoji[index]}</span>;
};
