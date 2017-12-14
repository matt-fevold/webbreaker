# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import getopt , sys

class ZeroBank2(unittest.TestCase):
    proxy='127.0.0.1:8090'
    def setUp(self):
        max_wait = 15
        service_args = [
            '--proxy='+self.proxy,
            '--proxy-type=http',
            '--ignore-ssl-errors=true'
        ]
        self.driver = webdriver.PhantomJS(service_args=service_args)
        #self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1920, 1080)
        self.driver.set_page_load_timeout(max_wait)
        self.driver.set_script_timeout(max_wait)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_zero_bank2(self):
        self.base_url = "http://zero.webappsecurity.com/"
        driver = self.driver
        driver.get(self.base_url + "/feedback.html")
        driver.find_element_by_link_text("Zero Bank").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    if len(sys.argv) > 0:
        ZeroBank2.proxy = sys.argv.pop()
    unittest.main()
