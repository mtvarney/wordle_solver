from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

WORDLE_URL = "https://www.nytimes.com/games/wordle/index.html"

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(WORDLE_URL)
time.sleep(5)
close = driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__b4z74")
close.click()

first_tile = driver.find_element(By.TAG_NAME, "body")
first_tile.send_keys("route")
first_tile.send_keys(Keys.ENTER)

soup = BeautifulSoup(driver.page_source)
soup.find_all()
time.sleep(100)