import time
import os

from unittest import skip

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('headless')
        options.add_argument('window-size=1366x768')

        self.browser = webdriver.Chrome(chrome_options=options)
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        try:
            table = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "id_list_table"))
            )
            rows = table.find_elements_by_tag_name('tr')
            self.assertIn(row_text, [row.text for row in rows])
        except TimeoutException:
            self.assertTrue(False)
