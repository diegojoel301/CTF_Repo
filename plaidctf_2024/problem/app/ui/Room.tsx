import React from "react";
import { DateTime, Duration } from "luxon";
import * as marked from "marked";

import { Icon } from "./Icon";
import { InviteUserDialog } from "./InviteUserDialog";
import { ChatInfo } from "./useChatInfo";
import { useClock } from "./useClock";
import { classes } from "./utils";

import styles from "./Room.module.scss";

interface Props {
	className?: string;
	chatInfo: ChatInfo;
	selectedRoom?: string;
	onSendMessage: (message: string) => void;
	onInviteUser: (room: string, user: string) => void;
	onLeaveRoom: () => void;
}

export const Room = (props: Props) => {
	const [value, setValue] = React.useState<string>("");
	const [scrolledToBottom, setScrolledToBottom] = React.useState<boolean>(true);
	const [showInviteUser, setShowInviteUser] = React.useState<boolean>(false);
	const messagesRef = React.useRef<HTMLDivElement>(null);

	const room = props.chatInfo.rooms?.find((room) => room.id === props.selectedRoom);

	React.useEffect(() => {
		if (scrolledToBottom) {
			messagesRef.current?.scrollTo(0, messagesRef.current.scrollHeight);
		}
	}, [room?.messages.messages, scrolledToBottom]);

	if (room === undefined) {
		return (
			<div className={classes(styles.room, styles.noRoomSelected, props.className)}>
				Select or create a room to begin chatting
			</div>
		);
	}

	let messageGroups: { from: string, timestamp: DateTime, messages: { timestamp: DateTime, content: string }[] }[] = [];

	for (const message of room.messages.messages) {
		const lastGroup = messageGroups[messageGroups.length - 1];
		const lastMessage = lastGroup?.messages[lastGroup.messages.length - 1];

		if (
			lastGroup === undefined
			|| lastGroup.from !== message.from
			|| lastMessage === undefined
			|| message.timestamp.diff(lastMessage.timestamp) > Duration.fromObject({ minutes: 5 })
		) {
			messageGroups.push({
				from: message.from,
				timestamp: message.timestamp,
				messages: [{ timestamp: message.timestamp, content: message.content }],
			});
		} else {
			lastGroup.messages.push({ timestamp: message.timestamp, content: message.content });
		}
	}

	return (
		<div className={classes(styles.room, props.className)}>
			<div
				ref={messagesRef}
				className={styles.messages}
				onScroll={(event) => {
					const element = event.target as HTMLDivElement;
					setScrolledToBottom(element.clientHeight - (element.scrollHeight - element.scrollTop) < 10);
				}}
			>
				{
					messageGroups.map((group, index) => (
						<MessageGroup
							key={index}
							from={group.from}
							timestamp={group.timestamp}
							messages={group.messages}
						/>
					))
				}
			</div>
			<div className={styles.input}>
				<input
					className={styles.inputField}
					type="text"
					name="message"
					value={value}
					onChange={(event) => setValue(event.target.value)}
					placeholder="Type a message..."
					onKeyDown={(event) => {
						if (event.key === "Enter") {
							props.onSendMessage(value);
							setValue("");
						}
					}}
				/>
			</div>
			<div className={styles.users}>
				{
					room.users.map((user) => (
						<div key={user} className={styles.user}>
							{user}
						</div>
					))
				}
				<div className={styles.inviteUser} onClick={() => setShowInviteUser(true)}>
					<Icon name="person_add" />
					Invite User
				</div>
				<div className={styles.leaveRoom} onClick={props.onLeaveRoom}>
					<Icon name="exit_to_app" />
					Leave Room
				</div>
			</div>
			{
				showInviteUser
					? (
						<InviteUserDialog
							onClose={() => setShowInviteUser(false)}
							onInviteUser={(name) => {
								props.onInviteUser(props.selectedRoom!, name);
								setShowInviteUser(false);
							}}
						/>
					)
					: null
			}
		</div>
	);
};

interface MessageGroupProps {
	className?: string;
	from: string;
	timestamp: DateTime;
	messages: {
		timestamp: DateTime;
		content: string;
	}[];
}

const MessageGroup = (props: MessageGroupProps) => {
	const clock = useClock();

	return (
		<div className={classes(styles.messageGroup, props.className)}>
			<div className={styles.from}>{props.from}</div>
			<div className={styles.timestamp}>
				{
					props.timestamp.startOf("day").equals(clock.startOf("day"))
						? props.timestamp.toLocaleString(DateTime.TIME_SIMPLE)
						: props.timestamp.toLocaleString(DateTime.DATETIME_SHORT)
				}
			</div>
			<div className={styles.contents}>
				{
					props.messages.map((message, index) => (
						<div
							key={index}
							className={styles.message}
							dangerouslySetInnerHTML={{ __html: marked.parse(message.content) }}
						/>
					))
				}
			</div>
		</div>
	);
};