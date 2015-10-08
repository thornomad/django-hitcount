# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class UpdateHitCountSelenium(StaticLiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.delay = 3

    def tearDown(self):
        self.selenium.quit()

    def test_ajax_hit(self):
        self.selenium.get("%s%s" % (self.live_server_url, '/1/'))
        wait = WebDriverWait(self.selenium, 3)
        response = wait.until(EC.text_to_be_present_in_element((By.ID, 'hit-counted-value'), 'true'))
        self.assertTrue(response)
