import { DateTime } from "luxon";
import React from "react";

import { FullMoonGate } from "./FullMoonGate";
import { Icon } from "./Icon";
import { Layout } from "./Layout";
import { Loader } from "./Loader";
import { Room } from "./Room";
import { RoomList } from "./RoomList";
import { Settings } from "./Settings";
import { useChatInfo } from "./useChatInfo";
import { SessionProvider } from "./useSession";
import { useWebsocket } from "./useWebsocket";
import { api } from "./utils";

import styles from "./Chat.module.scss";

export const Chat = () => (
	<SessionProvider>
		<FullMoonGate>
			<ChatIntl />
		</FullMoonGate>
	</SessionProvider>
);

const ChatIntl = () => {
	const ws = useWebsocket();
	const { chatInfo, loadHistoryForRoom, onMessage, onJoinRoom, onLeaveRoom, onUserJoined, onUserLeft, setRoom } = useChatInfo();
	const [showSettings, setShowSettings] = React.useState<boolean>(false);

	const roomInfo = chatInfo.rooms?.find((rm) => rm.id === chatInfo.currentRoom);

	const changeRoom = React.useCallback((room: string) => {
		setRoom(room);
		loadHistoryForRoom(room);
	}, [setRoom, loadHistoryForRoom]);

	React.useEffect(() => {
		if (ws !== undefined) {
			ws.addEventListener("message", (event) => {
				const { seq, data } = JSON.parse(event.data);
				ws.send(JSON.stringify({ kind: "Ack", seq }));

				switch (data.kind) {
					case "Message": {
						onMessage({
							room: data.room,
							from: data.sender,
							content: data.content,
							timestamp: DateTime.fromMillis(data.timestamp),
						});
						break;
					}

					case "RoomCreated": {
						onJoinRoom({
							id: data.id,
							name: data.name,
							users: data.users,
						});
						setRoom(data.id);
						break;
					}

					case "RoomJoined": {
						onJoinRoom({
							id: data.room.id,
							name: data.room.name,
							users: data.users,
						});
						break;
					}

					case "RoomLeft": {
						onLeaveRoom(data.room);
						if (chatInfo.currentRoom === data.room) {
							setRoom(undefined);
						}
						break;
					}

					case "UserJoinedRoom": {
						onUserJoined(data.room, data.user);
						break;
					}

					case "UserLeftRoom": {
						onUserLeft(data.room, data.user);
						break;
					}
				}
			});
		}
	}, [ws]);

	if (ws === undefined) {
		return (
			<Layout className={styles.chat}>
				<div className={styles.loading}>
					Loading... <Loader />
				</div>
			</Layout>
		);
	} else {
		return (
			<Layout
				className={styles.chat}
				sidebar={
					<RoomList
						className={styles.rooms}
						chatInfo={chatInfo}
						selectedRoom={chatInfo.currentRoom}
						onSelectRoom={(room) => changeRoom(room.id)}
						onCreateRoom={(name) => {
							ws.send(JSON.stringify({
								kind: "CreateRoom",
								name,
							}));
						}}
					/>
				}
				header={
					<div className={styles.header}>
						<div className={styles.title}>
							{roomInfo?.name}
						</div>
						<div
							className={styles.settings}
							onClick={() => setShowSettings(true)}
						>
							<Icon name="settings" />
						</div>
						<div
							className={styles.logOut}
							onClick={async () => {
								await api("POST", "logout");
								// go back to home and force a reload
								window.location.href = "/";
							}}
						>
							<Icon name="logout" />
						</div>
					</div>
				}
			>
				<Room
					className={styles.messages}
					chatInfo={chatInfo}
					selectedRoom={chatInfo.currentRoom}
					onSendMessage={(content) => {
						if (chatInfo.currentRoom !== undefined) {
							ws.send(JSON.stringify({
								kind: "Message",
								room: chatInfo.currentRoom,
								content,
							}));
						}
					}}
					onInviteUser={(room, user) => {
						ws.send(JSON.stringify({
							kind: "AddToRoom",
							room,
							user,
						}));
					}}
					onLeaveRoom={() => {
						if (chatInfo.currentRoom !== undefined) {
							ws.send(JSON.stringify({
								kind: "LeaveRoom",
								room: chatInfo.currentRoom,
							}));
							setRoom(undefined);
						}
					}}
				/>
				{
					showSettings
						? <Settings />
						: null
				}
			</Layout>
		);
	}
};
