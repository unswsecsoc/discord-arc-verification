DROP TRIGGER update_timestamp ON users;
DROP TRIGGER update_timestamp ON clubs;

DROP TABLE members;
DROP TABLE clubs;
DROP TABLE users;

DROP FUNCTION trigger_set_timestamp;