import React from "react";

const LocationContext = React.createContext<{ location: { latitude: number, longitude: number } | undefined, declined: boolean } | undefined>(undefined);

export const LocationProvider = (props: { children: React.ReactNode }) => {
	const [location, setLocation] = React.useState<{ latitude: number, longitude: number } | undefined>(undefined);
	const [declined, setDeclined] = React.useState(false);

	React.useEffect(() => {
		navigator.geolocation.getCurrentPosition(
			(position) => {
				setLocation({
					latitude: position.coords.latitude,
					longitude: position.coords.longitude,
				});
			},
			() => {
				setDeclined(true);
			},
		);
	}, []);

	return (
		<LocationContext.Provider value={{ location, declined }}>
			{props.children}
		</LocationContext.Provider>
	);
}

export const useLocation = () => {
	const location = React.useContext(LocationContext);

	if (location === undefined) {
		throw new Error("useLocation must be used within a LocationProvider");
	}

	return location;
};
