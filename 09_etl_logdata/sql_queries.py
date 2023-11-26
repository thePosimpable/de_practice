# dropping tables
staging_logs_drop = "DROP TABLE IF EXISTS staging_logs;"

# creating tables
staging_logs_create = """
	CREATE TABLE IF NOT EXISTS staging_logs (
		ts TIMESTAMP NOT NULL,
		app_module VARCHAR,
		action VARCHAR,
		username VARCHAR,
		log_entry VARCHAR NOT NULL
	);
"""

staging_logs_insert = ("""
	INSERT INTO staging_logs (ts, app_module, action, username, log_entry) VALUES (%s, %s, %s, %s, %s);
""")

create_table_queries = [staging_logs_create]
drop_table_queries = [staging_logs_drop]