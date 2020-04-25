ALTER TABLE users
	ADD COLUMN full_name VARCHAR(70) NOT NULL,
	ADD COLUMN zid_verified BOOLEAN NOT NULL DEFAULT FALSE,
	ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE,
	ADD COLUMN phone_verified BOOLEAN NOT NULL DEFAULT FALSE;

UPDATE users SET full_name=given_name || ' ' || family_name, zid_verified=is_verified;
ALTER TABLE users DROP COLUMN given_name, DROP COLUMN family_name;
ALTER TABLE clubs ADD COLUMN unsw_only BOOLEAN NOT NULL DEFAULT FALSE;

CREATE OR REPLACE FUNCTION cleanup_records() RETURNS VOID AS $$
BEGIN
	DELETE FROM users WHERE is_verified=FALSE AND updated_at + INTERVAL '1' HOUR < NOW();
END
$$ LANGUAGE PLPGSQL;
