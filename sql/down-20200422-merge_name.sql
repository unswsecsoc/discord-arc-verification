DROP FUNCTION cleanup_records;

ALTER TABLE users
	ADD COLUMN given_name VARCHAR(32) NOT NULL,
	ADD COLUMN family_name VARCHAR(32);

UPDATE users SET 
  given_name=SUBSTRING(full_name FROM 1 FOR 
    (CASE WHEN STRPOS(full_name, ' ') - 1 >= 0 
      THEN STRPOS(full_name, ' ') - 1
      ELSE CHAR_LENGTH(full_name) 
    END)
  ),     
  family_name=SUBSTRING(full_name FROM 
    STRPOS(full_name, ' ') + 1
    FOR CHAR_LENGTH(full_name) - (CASE WHEN STRPOS(full_name, ' ') - 1 >= 0 
      THEN STRPOS(full_name, ' ') - 1
      ELSE CHAR_LENGTH(full_name)
    END));

ALTER TABLE users 
	DROP COLUMN full_name,
	ADD COLUMN zid_verified,
	ADD COLUMN email_verified,
	ADD COLUMN phone_verified;
ALTER TABLE clubs DROP COLUMN unsw_only;
