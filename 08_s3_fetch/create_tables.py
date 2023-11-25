import psycopg2, configparser
from sql_queries import create_table_queries, drop_table_queries

def create_database(config):
	conn = psycopg2.connect(
		user = config.get('POSTGRES', 'USER'),
		password = config.get('POSTGRES', 'PASSWORD'),
		port = config.get('POSTGRES', 'PORT'),
		database = config.get('POSTGRES', 'DATABASE')
	)

	conn.set_session(autocommit = False)
	cur = conn.cursor()

	return cur, conn

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

	cur, conn = create_database(config)
	
	drop_tables(cur, conn)
	create_tables(cur, conn)

	conn.close()

if __name__ == "__main__":
	main()