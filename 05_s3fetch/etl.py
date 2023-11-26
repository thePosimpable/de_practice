import boto3
import pandas
import io
import pyarrow, fastparquet
import configparser
import psycopg2

from dotenv import load_dotenv
from sql_queries import *

DOTENV_PATH = ".env"
load_dotenv(DOTENV_PATH)

def fetch_from_s3(config, buffer):
	s3 = boto3.resource(
		's3',
		region_name = config.get('AWS', 'REGION'),
		aws_access_key_id = config.get('AWS', 'ACCESS_KEY'),
		aws_secret_access_key = config.get('AWS', 'SECRET')
	)

	# https://registry.opendata.aws/speedtest-global-performance/
	bucketName = "ookla-open-data"
	filepath = "parquet/performance/type=fixed/year=2019/quarter=1/2019-01-01_performance_fixed_tiles.parquet"

	object = s3.Object(bucketName, filepath)
	object.download_fileobj(buffer)

	return buffer

def load_to_db(cur, conn):
	cur.execute(staging_ookla_copy)
	conn.commit()

def main():
	config = configparser.ConfigParser()
	config.read('aws.cfg')

	buffer = io.BytesIO()
	buffer = fetch_from_s3(config, buffer)

	df = pandas.read_parquet(buffer)
	df.to_csv("test.csv", index = False)

	main2()

def main2():
	conn = psycopg2.connect(
		user = os.environ.get("DB_USER"),
		password = os.environ.get("DB_PASS"),
		port = os.environ.get("DB_PORT"),
		database = os.environ.get("DB_DATABASE")
	)

	cur = conn.cursor()

	load_to_db(cur, conn)

	conn.close()

if __name__ == "__main__":
	# main()
	main2()