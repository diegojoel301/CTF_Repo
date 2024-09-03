import React from "react";
import { RouterProvider, createBrowserRouter } from "react-router-dom";

import { Chat } from "./Chat";
import { Home } from "./Home";
import { Login } from "./Login";
import { Register } from "./Register";
import { Reset } from "./Reset";
import { ClockProvider } from "./useClock";
import { LocationProvider } from "./useLocation";
import { LunarInfoProvider } from "./useLunarInfo";
import { SelfProvider } from "./useSelf";

import "./App.module.scss";

const router = createBrowserRouter([
	{
		path: "/",
		Component: Home
	},
	{
		path: "/login",
		Component: Login
	},
	{
		path: "/reset",
		Component: Reset
	},
	{
		path: "/register",
		Component: Register
	},
	{
		path: "/chat",
		Component: Chat
	}
]);

export const App = () => (
	<SelfProvider>
		<ClockProvider>
			<LocationProvider>
				<LunarInfoProvider>
					<RouterProvider router={router} />
				</LunarInfoProvider>
			</LocationProvider>
		</ClockProvider>
	</SelfProvider>
);
