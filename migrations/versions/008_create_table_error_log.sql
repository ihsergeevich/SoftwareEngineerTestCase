CREATE TABLE IF NOT EXISTS error_log (
	launch_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"date" date,
	symbol varchar(64),
	message text
);