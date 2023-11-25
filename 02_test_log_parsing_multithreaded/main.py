import re, time, math
import pandas as pd
from threading import Thread, Barrier, Lock

def read_file(file):
	with open(file) as f:
		f = f.readlines()

	return f

def process_data(data, processed_logs, mutex, barrier):
	for row in data:
		timestamp_pattern = "\[(.*?)\]"
		timestamp = re.search(timestamp_pattern, row).group(1)

		app_module_pattern = ":\s[a-zA-Z]+:"
		app_module = "" if re.search(app_module_pattern, row)  is None else (re.search(app_module_pattern, row)[0].replace(":", " ")).replace(" ", "")

		action_pattern = "[A-Z]{5,}"
		action = re.findall(action_pattern, row)
		action = None if len(action) == 0 else action[0]

		user_pattern = "BY user [a-zA-Z]+"
		user = re.findall(user_pattern, row)

		if len(user) == 0:
			try:
				user = row.split("User")[1]
				user = user.split("authenticated.")[0]

			except:
				user = None
		
		else:
			user = user[0].split("BY user")[1]

		test_split = row.split("BY")[0]
		test_split = test_split.split("local.INFO:")[1]

		try:
			log = test_split.split(": ")[1]

		except:
			action = "AUTH"
			log = "AUTH"
			
		# print(timestamp, app_module, action, user, log)

		mutex.acquire()
		processed_logs.append((timestamp, app_module, action, user, log))
		mutex.release()
		
	barrier.wait()

def main():
	start_time = time.time()
	data = read_file("../api_logs.log");

	threads = 12

	processed_logs = []

	mutex = Lock()
	barrier = Barrier(threads + 1)
	
	start = 0
	end = int(math.ceil(len(data)/threads))
	for counter in range(0, threads):
		Thread(target = process_data, args = (data[start:end], processed_logs, mutex, barrier)).start()
		start = end + 1
		end += int(math.ceil(len(data)/threads))

	barrier.wait()
	end_time = time.time()
	print("multiparallel end, time taken", end_time - start_time)

	df = pd.DataFrame(processed_logs, columns=["timestamp", "app_module", "action", "user", "log"])
	df.to_csv("test.csv")

	

if __name__ == "__main__":
	main()

	
	