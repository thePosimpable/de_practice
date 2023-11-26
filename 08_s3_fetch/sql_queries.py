# dropping tables
staging_ookla_drop = "DROP TABLE IF EXISTS staging_ookla;"

# creating tables
staging_ookla_create = """
	CREATE TABLE IF NOT EXISTS staging_ookla (
		quadkey TEXT NOT NULL,
		tile TEXT NOT NULL,
		avg_d_kbps TEXT NOT NULL,
		avg_u_kbps TEXT NOT NULL,
		avg_lat_ms TEXT NOT NULL,
		tests TEXT NOT NULL,
		devices TEXT NOT NULL
	);
"""

staging_ookla_copy = ("""
	COPY staging_ookla (
		quadkey,
		tile,
		avg_d_kbps,
		avg_u_kbps,
		avg_lat_ms,
		tests,
		devices
	)

	FROM 'C:/Users/Public/test.csv'
	WITH NULL AS ' ' CSV
	HEADER;
""")

# https://hackersandslackers.com/psycopg2-postgres-python/
staging_ookla_copy2 = ("""
	COPY %s (
		quadkey,
		tile,
		avg_d_kbps,
		avg_u_kbps,
		avg_lat_ms,
		tests,
		devices
	)

	FROM STDIN
	WITH NULL AS ' ' CSV
	HEADER;
""")

create_table_queries = [staging_ookla_create]
drop_table_queries = [staging_ookla_drop]