import React from "react";

interface Props {
	to: string;
}

export const Redirect = (props: Props) => {
	window.location.assign(props.to);
	return null;
};
