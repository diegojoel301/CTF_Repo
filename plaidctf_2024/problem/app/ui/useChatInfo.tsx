import { DateTime } from "luxon";
import React from "react";

import { api } from "./utils";

export interface Room {
	id: string;
	name: string;
	users: string[];
}

export interface ChatInfo {
	rooms?: RoomInfo[];
	currentRoom?: string;
	queue?: ReducerAction[];
}

interface RoomInfo {
	id: string;
	name: string;
	messages: {
		messages: MessageInfo[];
		loading: boolean;
		complete: boolean;
	};
	hasUnread: boolean;
	users: string[];
}

interface MessageInfo {
	timestamp: DateTime;
	from: string;
	content: string;
}

type ReducerAction =
	| { type: "initialize"; rooms: Room[] }
	| { type: "addMessage"; room: string; message: MessageInfo }
	| { type: "startLoadingHistory"; room: string }
	| { type: "finishLoadingHistory"; room: string; messages: MessageInfo[] }
	| { type: "joinRoom"; room: Room }
	| { type: "leaveRoom"; room: string }
	| { type: "userJoined"; room: string; user: string }
	| { type: "userLeft"; room: string; user: string }
	| { type: "setRoom"; room?: string }
	;

function reduceChatInfo(state: ChatInfo, action: ReducerAction): ChatInfo {
	if (state.rooms === undefined) {
		switch (action.type) {
			case "initialize": {
				let newState: ChatInfo = {
					rooms: (
						action.rooms
						.map((room) => ({
							id: room.id,
							name: room.name,
							messages: {
								messages: [],
								loading: false,
								complete: false,
							},
							hasUnread: false,
							users: room.users,
						}))
						.sort((a, b) => a.name.localeCompare(b.name))
					),
				};

				if (state.queue !== undefined) {
					newState = state.queue.reduce(reduceChatInfo, newState);
				}

				return newState;
			}

			default: {
				return {
					...state,
					queue: [...(state.queue ?? []), action],
				};
			}
		}
	} else {
		switch (action.type) {
			case "initialize": {
				console.error("Attempted to initialize chat info when already initialized");
				return state;
			}

			case "addMessage": {
				return {
					...state,
					rooms: state.rooms?.map((room) => {
						if (room.id === action.room) {
							return {
								...room,
								messages: {
									...room.messages,
									messages: [...room.messages.messages, action.message],
								},
								hasUnread: state.currentRoom !== action.room || room.hasUnread,
							};
						} else {
							return room;
						}
					}),
				};
			}

			case "startLoadingHistory": {
				return {
					...state,
					rooms: state.rooms?.map((room) => {
						if (room.id === action.room) {
							return {
								...room,
								messages: {
									...room.messages,
									loading: true,
								},
							};
						} else {
							return room;
						}
					}),
				};
			}

			case "finishLoadingHistory": {
				return {
					...state,
					rooms: state.rooms?.map((room) => {
						if (room.id === action.room) {
							return {
								...room,
								messages: {
									messages: [...action.messages, ...room.messages.messages],
									loading: false,
									complete: true,
								},
							};
						} else {
							return room;
						}
					}),
				};
			}

			case "joinRoom": {
				return {
					...state,
					rooms: (
						[
							...(state.rooms ?? []),
							{
								id: action.room.id,
								name: action.room.name,
								messages: {
									messages: [],
									loading: false,
									complete: false,
								},
								hasUnread: true,
								users: action.room.users
							},
						].sort((a, b) => a.name.localeCompare(b.name))
					)
				};
			};

			case "leaveRoom": {
				return {
					...state,
					rooms: state.rooms?.filter((room) => room.id !== action.room),
				};
			}

			case "userJoined": {
				return {
					...state,
					rooms: state.rooms?.map((room) => {
						if (room.id === action.room) {
							return {
								...room,
								users: [...room.users, action.user],
							};
						} else {
							return room;
						}
					}),
				};
			}

			case "userLeft": {
				return {
					...state,
					rooms: state.rooms?.map((room) => {
						if (room.id === action.room) {
							return {
								...room,
								users: room.users.filter((user) => user !== action.user),
							};
						} else {
							return room;
						}
					}),
				};
			}

			case "setRoom": {
				return {
					...state,
					currentRoom: action.room,
					rooms: state.rooms?.map((room) => ({
						...room,
						hasUnread: room.id === action.room ? false : room.hasUnread,
					})),
				};
			}
		}
	}
}

export const useChatInfo = () => {
	const [chatInfo, updateChatInfo] = React.useReducer(reduceChatInfo, {});

	React.useEffect(() => {
		api<Room[]>("GET", "rooms").then((rooms) => updateChatInfo({ type: "initialize", rooms }));
	}, []);

	const loadHistoryForRoom = (room: string) => {
		if (chatInfo.rooms === undefined) {
			return;
		}

		if (chatInfo.rooms.some((r) => r.id === room && r.messages.complete)) {
			return;
		}

		updateChatInfo({ type: "startLoadingHistory", room });

		api<{ messages: { timestamp: number; from: string; content: string }[] }>("GET", `room/${room}/history`)
			.then((data) => {
				updateChatInfo({
					type: "finishLoadingHistory",
					room,
					messages: data.messages.map((message) => ({
						timestamp: DateTime.fromMillis(message.timestamp),
						from: message.from,
						content: message.content,
					})),
				});
			});
	};

	const onMessage = (message: { room: string; timestamp: DateTime; from: string; content: string }) => {
		updateChatInfo({
			type: "addMessage",
			room: message.room,
			message: {
				timestamp: message.timestamp,
				from: message.from,
				content: message.content
			}
		});
	};

	const onJoinRoom = (room: Room) => {
		updateChatInfo({ type: "joinRoom", room });
	};

	const onLeaveRoom = (room: string) => {
		updateChatInfo({ type: "leaveRoom", room });
	};

	const onUserJoined = (room: string, user: string) => {
		updateChatInfo({ type: "userJoined", room, user });
	};

	const onUserLeft = (room: string, user: string) => {
		updateChatInfo({ type: "userLeft", room, user });
	};

	const setRoom = (room?: string) => {
		updateChatInfo({ type: "setRoom", room });
	};

	return {
		chatInfo,
		loadHistoryForRoom,
		onMessage,
		onJoinRoom,
		onLeaveRoom,
		onUserJoined,
		onUserLeft,
		setRoom,
	};
};
