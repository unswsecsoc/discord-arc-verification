ALTER TABLE users ADD COLUMN full_name VARCHAR(70) NOT NULL;
ALTER TABLE users ALTER COLUMN given_name DROP NOT NULL;

UPDATE users SET full_name=given_name || ' ' || family_name;

CREATE OR REPLACE FUNCTION cleanup_records() RETURNS VOID AS $$
BEGIN
	DELETE FROM users WHERE is_verified=FALSE AND updated_at + INTERVAL '1' HOUR < NOW();
END
$$ LANGUAGE PLPGSQL;