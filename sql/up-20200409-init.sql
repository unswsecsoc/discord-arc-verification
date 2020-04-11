CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE users (
	_id		SERIAL		PRIMARY KEY,
	given_name	VARCHAR(64)	NOT NULL,
	family_name	VARCHAR(64),
	zid		CHAR(8),
	arc_member	BOOLEAN		NOT NULL,
	email		VARCHAR(255),
	phone		VARCHAR(16),
	discord_id	VARCHAR(20)	UNIQUE,
	is_verified	BOOLEAN		NOT NULL DEFAULT FALSE,
	created_at	TIMESTAMP	NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP	NOT NULL DEFAULT CURRENT_TIMESTAMP,
	deleted_at	TIMESTAMP,

	CONSTRAINT 	zid_email_not_null CHECK (zid IS NOT NULL OR email IS NOT NULL),
	CONSTRAINT	zid_phone_not_null CHECK (zid IS NOT NULL OR phone IS NOT NULL)
);

CREATE TABLE clubs (
	_id			SERIAL		PRIMARY KEY,
	name			VARCHAR(40)	NOT NULL,
	permalink		VARCHAR(16)	NOT NULL UNIQUE,
	description		TEXT,
	email			VARCHAR(255)	NOT NULL,
	website			VARCHAR(255)	NOT NULL,
	admin_channel_id	VARCHAR(20),
	admin_role_id		VARCHAR(20),
	verified_role_id	VARCHAR(20),
	discord_id		VARCHAR(20)	UNIQUE,
	is_enabled		BOOLEAN		NOT NULL,
	created_at		TIMESTAMP	NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at		TIMESTAMP	NOT NULL DEFAULT CURRENT_TIMESTAMP,
	deleted_at		TIMESTAMP
);

CREATE TABLE members (
	user_id		INTEGER		REFERENCES users(_id) ON DELETE CASCADE,
	club_id		INTEGER		REFERENCES clubs(_id) ON DELETE CASCADE,
	created_at	TIMESTAMP	NOT NULL DEFAULT CURRENT_TIMESTAMP,
	deleted_at	TIMESTAMP,

	UNIQUE(user_id, club_id)
);

CREATE TRIGGER update_timestamp BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();
CREATE TRIGGER update_timestamp BEFORE UPDATE ON clubs FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();