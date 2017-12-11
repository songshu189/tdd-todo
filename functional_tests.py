import time
from selenium import webdriver
options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('headless')
options.add_argument('window-size=1366x768')

browser = webdriver.Chrome(chrome_options=options)
browser.get('http://localhost:8080')
time.sleep(2)

assert 'Django' in browser.title

browser.quit()