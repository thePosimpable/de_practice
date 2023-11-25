import re, time, psycopg2
from sql_queries import *

def process_logfile(file):
	with open(file) as f:
		f = f.readlines()

	return f

def process_parsed_data(parsed_data, cur, conn):
	for line in parsed_data:
		line = line.replace("Customers Module", "CustomerController")
		line = line.replace("Customer DRs Module - Customer DRs", "DeliveryReceiptController")
		line = line.replace("Products Module - Product Categories", "CategoryController")

		timestamp_pattern = "\[(.*?)\]"
		timestamp = re.search(timestamp_pattern, line).group(1)

		app_module_pattern = ":\s[a-zA-Z.]+:"
	
		if re.search(app_module_pattern, line) == None:
			app_module = "AUTH"
			
		else:
			app_module = (re.search(app_module_pattern, line)[0].replace(":", " ")).replace(" ", "")

		action_pattern = "[A-Z]{5,}"
		action = re.findall(action_pattern, line)

		action = None if len(action) == 0 else action[0]

		user_pattern = "BY user [a-zA-Z]+"
		user = re.findall(user_pattern, line)

		if len(user) > 0:
			user = user[0].split("BY user ")[1]
			user = user.strip()
		 
		else:
			if app_module == "AUTH":
				user = line.split("User")[1]
				user = user.split("authenticated.")[0]
				user = user.strip()

			else:
				if len(re.findall("DB transaction failed", line)) > 0:
					user = line.split()[4]
					user = user.strip()

				else:
					user = None
		
		if app_module != "AUTH":
			if len(re.findall("DB transaction failed", line)) > 0:
				log = "DB transaction failed"

			else:
				log = line.split(app_module + ": ")[1]
				log = log.split("BY")[0]

		else:
			action = "AUTH"
			log = "AUTH"
			
		cur.execute(staging_logs_insert, (timestamp, app_module, action, user, log))
		
	conn.commit()

def main():
	conn = psycopg2.connect(
		user = "postgres",
		password = "password",
		port = "5432",
		database = "test_log_db1"
	)

	cur = conn.cursor()

	filepath = "../api_logs.log"
	processed_data = process_logfile(filepath)

	process_parsed_data(processed_data, cur, conn)

	conn.close()

if __name__ == "__main__":
	start_time = time.time()

	main()

	end_time = time.time()
	print("end, time taken", end_time - start_time)