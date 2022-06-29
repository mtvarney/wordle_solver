import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# Grabs absent, present, and correct letters to narrow down word list to only words that match that criteria

def update_trimmed_list(list_trimmed):
    soup = BeautifulSoup(driver.find_element(By.XPATH, "//body").get_attribute('outerHTML'), "html.parser")
    absent_letters = []
    present_letters = []
    correct_letters = {}
    for data in soup.find_all(attrs={'data-state': 'correct', 'class': 'Tile-module_tile__3ayIZ'}):
        parent = data.find_parent()
        letter_idx = parent["style"].find(' ') + 1
        location = int(parent["style"][letter_idx])
        if location not in correct_letters:
            correct_letters[location] = data.get_text()
    for data in soup.find_all(attrs={'data-state': 'absent', 'class': 'Key-module_key__Rv-Vp Key-module_fade__37Hk8'}):
        if data.get_text() not in list(correct_letters.values()):
            absent_letters.append(data.get_text())
    for data in soup.find_all(attrs={'data-state': 'present', 'class': 'Key-module_key__Rv-Vp Key-module_fade__37Hk8'}):
        present_letters.append(data.get_text())

    trimmed_list = [word for word in list_trimmed if not any(ignore in word for ignore in absent_letters)]
    trimmed_list = [word for word in trimmed_list if all(present in word for present in present_letters)]
    for key, value in correct_letters.items():
        trimmed_list = [word for word in trimmed_list if word[key] == value]
    trimmed_list = [word for word in trimmed_list if word not in guesses]
    return trimmed_list


# Generates new random guess from trimmed down word list and sends the guess to wordle

def new_guess(list_trimmed):
    new_guess = random.choice(list_trimmed)
    guesses.append(new_guess)
    first_tile = driver.find_element(By.TAG_NAME, "body")
    first_tile.send_keys(new_guess)
    first_tile.send_keys(Keys.ENTER)


WORDLE_URL = "https://www.nytimes.com/games/wordle/index.html"

with open("wordle-answers-alphabetical.txt") as word_list:
    full_word_list = word_list.read().split("\n")

# Limit first guess to only words without repeated letters to get maximum information out of first guess

first_pass_word_list = [word for word in full_word_list if len(set(word)) == len(word)]

# Initialize webdriver and go to wordle website. Wait until initial popup comes up and close.

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(WORDLE_URL)
element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Modal-module_closeIcon__b4z74")))
close = driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__b4z74")
close.click()

time.sleep(1)

# Send first guess to wordle

guesses = []

first_tile = driver.find_element(By.TAG_NAME, "body")
first_guess = random.choice(first_pass_word_list)
guesses.append(first_guess)
first_tile.send_keys(first_guess)
first_tile.send_keys(Keys.ENTER)

time.sleep(2)

trimmed_list = full_word_list
trimmed_list = update_trimmed_list(trimmed_list)

# While loop to keep guessing until it sees the game completed popup

flag = True
while flag:
    time.sleep(1)
    try:
        driver.find_element(By.CLASS_NAME, "Stats-module_gameStats__ZP1aW")
        flag = False
    except NoSuchElementException:
        trimmed_list = update_trimmed_list(trimmed_list)
        new_guess(trimmed_list)

time.sleep(20)
