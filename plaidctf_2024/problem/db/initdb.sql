CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA werechat;

CREATE TABLE werechat.invite (
	code text not null
);

CREATE TABLE werechat.user (
	id text primary key,
	email text not null,
	password text not null, -- bcrypt
	settings jsonb not null default '{}',
	check (length(id) >= 3 and length(id) <= 32)
);

CREATE TABLE werechat.password_reset (
	user_id text not null references werechat.user(id),
	code text not null,
	created_at timestamptz not null default now(),
	primary key (user_id, code)
);

CREATE TABLE werechat.token (
	token text primary key default gen_random_uuid(),
	user_id text not null references werechat.user(id),
	created_at timestamptz not null default now()
);

CREATE TABLE werechat.room (
	id text primary key,
	name text not null
);

CREATE TABLE werechat.room_user (
	room_id text not null references werechat.room(id),
	user_id text not null references werechat.user(id),
	primary key (room_id, user_id)
);

CREATE TABLE werechat.message (
	id serial primary key,
	room_id text not null references werechat.room(id),
	user_id text not null references werechat.user(id),
	content text not null,
	timestamp timestamptz not null default now()
);

CREATE INDEX ON werechat.message (room_id, timestamp);

------------------------------------------------------------------------------

INSERT INTO werechat.invite (code) VALUES ('every_wolf_needs_a_pack');
