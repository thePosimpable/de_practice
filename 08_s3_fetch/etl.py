import boto3, pandas, io, pyarrow, fastparquet, configparser, psycopg2
from sql_queries import *

CSV_PATH = "C:/Users/Public/"
CSV_NAME = "test.csv"
STAGING_TABLE_NAME = "staging_ookla"

# https://registry.opendata.aws/speedtest-global-performance/
BUCKET = "ookla-open-data"
PARQUET_PATH = "parquet/performance/type=fixed/year=2019/quarter=1/2019-01-01_performance_fixed_tiles.parquet"

def fetch_from_s3(config, buffer):
	s3 = boto3.resource(
		's3',
		region_name = config.get('AWS', 'REGION'),
		aws_access_key_id = config.get('AWS', 'ACCESS_KEY'),
		aws_secret_access_key = config.get('AWS', 'SECRET')
	)

	object = s3.Object(BUCKET, PARQUET_PATH)
	object.download_fileobj(buffer)

	return buffer

def load_to_postgres(cur, conn):
	# poc for local postgres installation

	cur.execute(staging_ookla_copy)
	conn.commit()

def load_to_postgres2(cur, conn):
	# postgres db shifted from local machine installation to docker container instance

	f = open(f'{CSV_PATH}{CSV_NAME}', 'r')
	# docker exec -it some-postgres bash

	cur.copy_expert(sql = staging_ookla_copy2 % STAGING_TABLE_NAME, file = f)
	conn.commit()

def load_from_s3(config):
	buffer = io.BytesIO()
	buffer = fetch_from_s3(config, buffer)

	df = pandas.read_parquet(buffer)
	df.to_csv(CSV_NAME, index = False)

def load_to_staging(config):
	conn = psycopg2.connect(
		user = config.get('POSTGRES', 'USER'),
		password = config.get('POSTGRES', 'PASSWORD'),
		port = config.get('POSTGRES', 'PORT'),
		database = config.get('POSTGRES', 'DATABASE')
	)

	cur = conn.cursor()

	# load_to_postgres(cur, conn)
	load_to_postgres2(cur, conn)

	conn.close()

	print("Finished loading to Postgres DB.")

def main(config):
	# load_from_s3(config)
	load_to_staging(config)
	

if __name__ == "__main__":
	config = configparser.ConfigParser()
	config.read('appconfigs.cfg')

	main(config)