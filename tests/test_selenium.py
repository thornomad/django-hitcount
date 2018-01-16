# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
try:
    from django.core.urlresolvers import reverse
except ModuleNotFoundError:
    from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
                 "Skipping this test on Travis CI.")
class UpdateHitCountSelenium(StaticLiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.delay = 10

    def tearDown(self):
        self.selenium.quit()

    def test_ajax_hit(self):
        url = reverse('ajax', args=[1])
        self.selenium.get("%s%s" % (self.live_server_url, url))
        wait = WebDriverWait(self.selenium, self.delay)
        response = wait.until(EC.text_to_be_present_in_element((By.ID, 'hit-counted-value'), 'true'))
        self.assertTrue(response)
