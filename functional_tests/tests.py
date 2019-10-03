from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import TestCase

class NewVisitorLoginTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_email_and_password(self):

        driver = webdriver.Firefox()
        driver.get('http://localhost:8000')

        login_email_box = driver.find_element_by_name('login_email_box')
        self.assertIsNotNone(login_email_box)

        login_email_box.send_keys('test@emailhost.com')

        password_box = driver.find_element_by_name('login_password_box')
        self.assertIsNotNone(login_email_box)

        password_box.send_keys('password')

        # password_box.send_keys(Keys.RETURN) Wouldn't do anything



# Create your tests here.
