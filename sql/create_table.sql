CREATE TABLE IF NOT EXISTS aji.users (
	id serial,
	name text,
	address text
)
;

CREATE TABLE IF NOT EXISTS aji.admins (
	id serial,
	username text,
	pass text,
	name text
)
;