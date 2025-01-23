#!/usr/bin/env python3
import time
from configparser import ConfigParser

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os

import os

file_path = 'config.ini'
print("Datei existiert:", os.path.exists(file_path))
print("Datei lesbar:", os.access(file_path, os.R_OK))

# Load configuration
config = ConfigParser()
conf_file = open('config.ini')

with open('config.ini', 'r', encoding='utf-8') as f:
    config.read_file(f)


USERNAME = config.get('Login', 'email')
PASSWORD = config.get('Login', 'password')
LISTING_URL = config.get('Listing', 'listing_url')
DELAY = int(config.get('Driver', 'delay'))

# Login
driver = webdriver.Chrome()
driver.get('https://wg-gesucht.de')
# Remove cookie button
btn = driver.find_element(By.ID,"cmpbntyestxt").click()
driver.find_element(By.LINK_TEXT,"Mein Konto").click()
time.sleep(10)
username = driver.find_element(By.ID,"login_email_username")
password = driver.find_element(By.ID,"login_password")
username.send_keys(USERNAME)
password.send_keys(PASSWORD)
driver.find_element(By.ID,'login_submit').click()
time.sleep(5)

while True:
    # Open listing
    driver.get(
        LISTING_URL)
    time.sleep(3)
    contact = driver.find_element_by_class_name('bottom_contact_box')
    edit = contact.find_element_by_link_text('ANGEBOT BEARBEITEN')
    edit.send_keys(Keys.TAB)
    time.sleep(1)
    edit.click()
    time.sleep(3)

    # Refresh listing
    btn = driver.find_element_by_class_name('btn-orange') # weiter
    btn.send_keys(Keys.TAB)
    time.sleep(2)
    btn.send_keys(Keys.SPACE)
    btn = driver.find_element_by_class_name('btn-orange') # Änderungen ubernehmen
    btn.send_keys(Keys.TAB)
    time.sleep(2)
    btn.send_keys(Keys.SPACE)
    assert 'zehn Minuten' in driver.page_source
    print("Reloaded at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
    time.sleep(DELAY)
