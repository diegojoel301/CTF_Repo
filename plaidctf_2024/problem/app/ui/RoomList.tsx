import React from "react";

import { CreateRoomDialog } from "./CreateRoomDialog";
import { Icon } from "./Icon";
import { ChatInfo, Room } from "./useChatInfo";
import { classes } from "./utils";

import styles from "./RoomList.module.scss";

interface Props {
	className?: string;
	chatInfo: ChatInfo;
	selectedRoom?: string;
	onSelectRoom: (room: Room) => void;
	onCreateRoom: (name: string) => void;
}

export const RoomList = (props: Props) => {
	const [createRoomDialogOpen, setCreateRoomDialogOpen] = React.useState<boolean>(false);

	if (props.chatInfo.rooms === undefined) {
		return <p>Loading...</p>;
	} else {
		return (
			<div className={classes(styles.roomList, props.className)}>
				{
					props.chatInfo.rooms.map((room) => (
						<div
							key={room.id}
							className={classes(
								styles.room,
								props.selectedRoom === room.id ? styles.selected : undefined
							)}
							onClick={() => props.onSelectRoom(room)}
						>
							{room.name}
							{
								room.hasUnread
									? <Icon name="circle" className={styles.unread} />
									: null
							}
						</div>
					))
				}
				<div className={styles.createRoom} id="create-room" onClick={() => setCreateRoomDialogOpen(true)}>
					<Icon name="add_circle" />
					Create Room
				</div>
				{
					createRoomDialogOpen
						? (
							<CreateRoomDialog
								onClose={() => setCreateRoomDialogOpen(false)}
								onCreateRoom={(name) => {
									props.onCreateRoom(name);
									setCreateRoomDialogOpen(false);
								}}
							/>
						)
						: null
				}
			</div>
		);
	}
};