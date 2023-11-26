import bs4, requests, re, sys, datetime, time, copy, shutil, os
from dotenv import load_dotenv
from selenium import webdriver
from heroes import heroes

DOTENV_PATH = ".env"
load_dotenv(DOTENV_PATH)

opts = webdriver.ChromeOptions()
opts.headless = True
opts.log_level = 'OFF'

driver = webdriver.Chrome(os.environ.get("WEBDRIVER_PATH"), options = opts)

current_directory = os.getcwd()

def split_element(skill):
	skill = skill[1]
	element = copy.copy(skill)
	skill = skill.split('<div style="float:right;">')
	skill = skill[0]

	return (skill, element)

def process_skills(skills, hero):
	for skill in skills:
		skill = skill.get_attribute("innerHTML").split('<div style="font-weight: bold; font-size: 110%; border-bottom: 1px solid black; background: linear-gradient(-90deg, #1B1E21 -20%, #1B1E21 -20%, #1B1E21 -20%, #B44335) 90%; color: white; padding: 3px 5px;">')

		try:
			skill, element = split_element(skill)

			with open(f"skills_raw/{hero}_normal_{skill}.txt", "a", encoding = 'utf-8') as myfile:
				myfile.write(element)

		except:
			skill = " ".join(skill)

			try:
				skill = skill.split('<div style="font-weight: bold; font-size: 110%; border-bottom: 1px solid black; background: linear-gradient(-90deg, #1B1E21 -20%, #1B1E21 -20%, #1B1E21 -20%, #414141) 90%; color: white; padding: 3px 5px;">')

				skill, element = split_element(skill)

				try:
					with open(f"skills_raw/{hero}_ulti_{skill}.txt", "a", encoding = 'utf-8') as myfile:
						myfile.write(element)

				except:
					pass

			except:
				try:
					skill = " ".join(skill)

					skill = skill.split('<div style="font-weight: bold; font-size: 110%; border-bottom: 1px solid black; background: linear-gradient(-90deg, #1B1E21 -20%, #1B1E21 -20%, #1B1E21 -20%, #4b69ff) 90%; color: white; padding: 3px 5px;">')

					skill, element = split_element(skill)

					try:
						with open(f"skills_raw/{hero}_shard_{skill}.txt", "a", encoding = 'utf-8') as myfile:
							myfile.write(element)

					except:
						pass

				except:
					pass

def process_talents(talents, hero):
	for talent in talents:
		talent = talent.get_attribute("innerHTML")


		with open(f"talents_raw/{hero}_talents.txt", "a", encoding = 'utf-8') as myfile:
			myfile.write(talent)

def process_stats(stats, hero):
	for stat in stats:
		stat = stat.get_attribute("innerHTML")

		with open(f"stats_raw/{hero}_stats.txt", "a", encoding = 'utf-8') as myfile:
			myfile.write(stat)

def create_raw_dir(dir_name):
	path = os.path.join(current_directory, dir_name)

	shutil.rmtree(path)

	if not os.path.exists(path):
		os.mkdir(path)

def main():
	create_raw_dir("skills_raw")
	create_raw_dir("talents_raw")
	create_raw_dir("stats_raw")

	site = ""

	for hero in heroes:
		URL  = f"https://{site}/{hero}"

		driver.get(URL)

		skills = driver.find_elements_by_class_name('ability-background')
		process_skills(skills, hero)

		talents = driver.find_elements_by_class_name('wikitable')
		process_talents(talents, hero)

		stats = driver.find_elements_by_class_name('infobox')
		process_stats(stats, hero)
		
	print("===END SCRAPE===") 

if __name__ == "__main__":
	main()