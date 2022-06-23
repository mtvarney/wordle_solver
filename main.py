from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

WORDLE_URL = "https://www.nytimes.com/games/wordle/index.html"

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(WORDLE_URL)

