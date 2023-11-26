import requests, re, sys, datetime, re, os
import pandas as pd

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

DOTENV_PATH = ".env"
load_dotenv(DOTENV_PATH)

opts = webdriver.ChromeOptions()
opts.headless = True
opts.log_level = 'OFF'

driver = webdriver.Firefox(executable_path = os.environ.get("WEBDRIVER_PATH"))
BASE_URL = ""
PAGE_LIMIT = 2

def parse_price(price):
	regex = re.compile(r'\$?(?:(?:[1-9][0-9]{0,2})(?:,[0-9]{3})+|[1-9][0-9]*|0)(?:[\.,][0-9][0-9]?)?(?![0-9]+)')
	price = regex.findall(price)[0]
	price = price.replace(",", "")
	price = price.strip()
	price = float(price)

	return price

def create_directory(path):
	dir_exists = os.path.exists(path)

	if not dir_exists:
		os.makedirs(path)

	return path

def scrape_page(driver):
	listings = driver.find_elements_by_class_name('_3PztA')

	listings_list = []

	for listing in listings:
		html_string = listing.get_attribute("innerHTML")
		bs_object = BeautifulSoup(html_string)

		extracted_strings = bs_object.find_all(text = True)

		listing_tuple = (extracted_strings[0], parse_price(extracted_strings[1]))

		listings_list.append(listing_tuple)

	df = pd.DataFrame(listings_list, columns = ["product", "price"])

	dir_path = create_directory('data')
	ts_fn = str(datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))

	df.to_csv(f"{dir_path}/{ts_fn}.csv", encoding='utf-8-sig', index = False)

def main(keyword):
	global BASE_URL, PAGE_LIMIT
	final_url =  BASE_URL + "+".join(keyword.split(" "))
	final_url += "&rating=4"

	for page in range(1, PAGE_LIMIT + 1):
		page_url = final_url + f"&page={page}"
		driver.get(page_url)

	scrape_page(driver)

if __name__ == "__main__":
	main(keyword = sys.argv[1])

	# python scrape.py "nvme m2 ssd"