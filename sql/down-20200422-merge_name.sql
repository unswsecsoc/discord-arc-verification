DROP FUNCTION cleanup_records;

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

ALTER TABLE users DROP COLUMN full_name;
ALTER TABLE users ADD COLUMN IF NOT EXISTS given_name VARCHAR(32);
ALTER TABLE users ALTER COLUMN given_name SET NOT NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS family_name VARCHAR(32);