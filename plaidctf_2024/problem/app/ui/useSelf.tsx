import React from "react";

import { api } from "./utils";

export type FullMoonAction =
	| { kind: "Block" }
	| { kind: "Redirect"; url: string }
	| { kind: "Distract" }
	;

export interface Self {
	id: string;
	settings?: {
		fullMoonAction?: FullMoonAction;
		timezone?: string;
	};
}

const SelfContext = React.createContext<{ loading: boolean, self?: Self, refresh: () => void } | undefined>(undefined);

interface SelfProviderProps {
	children: React.ReactNode;
}

export const SelfProvider = (props: SelfProviderProps) => {
	const [loading, setLoading] = React.useState<boolean>(true);
	const [self, setSelf] = React.useState<Self | undefined>(undefined);

	const refresh = React.useCallback(() => {
		setLoading(true);
		api<Self>("GET", "self")
			.then((self) => {
				setSelf(self);
				setLoading(false);
			})
			.catch(() => {
				setSelf(undefined);
				setLoading(false);
			});
	}, []);

	React.useEffect(() => {
		refresh();
	}, [refresh]);

	return (
		<SelfContext.Provider value={{ loading, self, refresh }}>
			{props.children}
		</SelfContext.Provider>
	);
};

export const useSelf = () => {
	const self = React.useContext(SelfContext);

	if (self === undefined) {
		throw new Error("useSelf must be used within a SelfProvider");
	}

	return self;
};
