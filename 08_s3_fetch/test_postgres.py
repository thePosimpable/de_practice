import psycopg2, configparser
from sql_queries import create_table_queries, drop_table_queries

def create_database(config):
	try:
		conn = psycopg2.connect(
			user = config.get('POSTGRES', 'USER'),
			password = config.get('POSTGRES', 'PASSWORD'),
			port = config.get('POSTGRES', 'PORT'),
			database = config.get('POSTGRES', 'DATABASE')
		)

		print(f"{config.get('POSTGRES', 'DATABASE')} Postgres instance is UP.")
		conn.close()

	except:
		print(f"Could not establish connection with {config.get('POSTGRES', 'DATABASE')} Postgres DB.")

def drop_tables(cur, conn):
	for query in drop_table_queries:
		cur.execute(query)
		conn.commit()

def create_tables(cur, conn):
	for query in create_table_queries:
		cur.execute(query)
		conn.commit()

def main():
	config = configparser.ConfigParser()
	config.read('appconfigs.cfg')

	create_database(config)

if __name__ == "__main__":
	main()