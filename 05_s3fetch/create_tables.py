import psycopg2
from dotenv import load_dotenv
from sql_queries import create_table_queries, drop_table_queries

DOTENV_PATH = ".env"
load_dotenv(DOTENV_PATH)

def create_database():
	conn = psycopg2.connect(
		user = os.environ.get("DB_USER"),
		password = os.environ.get("DB_PASS"),
		port = os.environ.get("DB_PORT"),
		database = os.environ.get("DB_DATABASE")
	)

	conn.set_session(autocommit=True)
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
	cur, conn = create_database()
	
	drop_tables(cur, conn)
	create_tables(cur, conn)

	conn.close()

if __name__ == "__main__":
	main()