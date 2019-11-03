from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.auth.hashers import make_password
import time
from login.models import User

class NewVisitorLoginTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_email_and_password(self):

        self.browser.get(self.live_server_url + '/login/')
        time.sleep(2)

        login_email_box = self.browser.find_element_by_id('login_email_box')
        self.assertIsNotNone(login_email_box)

        login_email_box.send_keys('test@emailhost.com')
        time.sleep(1)

        password_box = self.browser.find_element_by_id('login_password_box')
        self.assertIsNotNone(login_email_box)

        password_box.send_keys('password')


        # password_box.send_keys(Keys.RETURN) Wouldn't do anything

    def test_enter_credentials_failed_login_displays_failure_message(self):

        self.browser.get(self.live_server_url + '/login/')
        time.sleep(2)

        login_email_box = self.browser.find_element_by_id('login_email_box')
        self.assertIsNotNone(login_email_box)

        login_email_box.send_keys('test@emailhost.com')
        time.sleep(1)

        password_box = self.browser.find_element_by_id('login_password_box')
        self.assertIsNotNone(password_box)

        password_box.send_keys('password')

        submit_button = self.browser.find_element_by_id('login_submit_button')
        self.assertIsNotNone(submit_button)

        submit_button.click()
        time.sleep(2)

        failed_login_paragraph = self.browser.find_element_by_id('failed_login_paragraph')
        self.assertIsNotNone(failed_login_paragraph)

        failed_login_text = failed_login_paragraph.text

        self.assertEqual(failed_login_text, "Incorrect login credentials")
    
    def test_enter_credentials_successful_login_redirects_to_home(self):

        email = "test@testhost.com"
        password = "password"
        self.browser.get(self.live_server_url + '/login/')
        time.sleep(1)

        User.objects.create(email=email, hashed_password=make_password(password))
        print(self.live_server_url)
        login_email_box = self.browser.find_element_by_id('login_email_box')
        self.assertIsNotNone(login_email_box)

        login_email_box.send_keys(email)
        time.sleep(1)

        password_box = self.browser.find_element_by_id('login_password_box')
        self.assertIsNotNone(password_box)

        password_box.send_keys(password)

        submit_button = self.browser.find_element_by_id('login_submit_button')
        self.assertIsNotNone(submit_button)

        self.assertIsNotNone(User.objects.get(email=email))

        submit_button.click()

        time.sleep(1)

        self.assertEqual(self.browser.current_url, self.live_server_url + '/home/')

    def test_new_user_create_credentials_and_login_redirects_to_home(self):

        name = "Test Testington"
        email = "test@testhost.com"
        password = "password"

        self.browser.get(self.live_server_url + '/login/')
        time.sleep(1)

        new_user_link = self.browser.find_element_by_id('new_user_link')
        self.assertIsNotNone(new_user_link)

        new_user_link.click()
        time.sleep(1)

        self.assertEqual(self.browser.current_url, self.live_server_url + '/login/new/')

        name_input = self.browser.find_element_by_id('new_user_name_field')
        self.assertIsNotNone(name_input)

        name_input.send_keys(name)
        time.sleep(1)

        email_input = self.browser.find_element_by_id('new_user_email_field')
        self.assertIsNotNone(email_input)

        email_input.send_keys(email)
        time.sleep(1)

        password_input = self.browser.find_element_by_id('new_user_password_field')
        self.assertIsNotNone(password_input)

        password_input.send_keys(password)
        time.sleep(1)

        new_user_submit_button = self.browser.find_element_by_id('new_user_submit_button')
        self.assertIsNotNone(new_user_submit_button)

        new_user_submit_button.click()
        time.sleep(1)

        self.assertEqual(self.browser.current_url, self.live_server_url + '/home/')

    def test_new_user_create_credentials_and_login_missing_fields_highlight_and_message(self):
        blank_name = ""
        email = "test@testhost.com"
        password = "password"

        self.browser.get(self.live_server_url + '/login/')
        time.sleep(1)

        new_user_link = self.browser.find_element_by_id('new_user_link')
        self.assertIsNotNone(new_user_link)

        new_user_link.click()
        time.sleep(1)

        self.assertEqual(self.browser.current_url, self.live_server_url + '/login/new/')

        name_input = self.browser.find_element_by_id('new_user_name_field')
        self.assertIsNotNone(name_input)

        name_input.send_keys(blank_name)
        time.sleep(1)

        email_input = self.browser.find_element_by_id('new_user_email_field')
        self.assertIsNotNone(email_input)

        email_input.send_keys(email)
        time.sleep(1)

        password_input = self.browser.find_element_by_id('new_user_password_field')
        self.assertIsNotNone(password_input)

        password_input.send_keys(password)
        time.sleep(1)

        new_user_submit_button = self.browser.find_element_by_id('new_user_submit_button')
        self.assertIsNotNone(new_user_submit_button)

        new_user_submit_button.click()
        time.sleep(1)

        name_input = self.browser.find_element_by_id('new_user_name_field')
        name_input_class = name_input.get_attribute("class")

        self.assertEqual(name_input_class, "invalid-or-missing")        

    def test_new_user_create_credentials_and_login_invalid_email_highlight_and_message(self):
        pass

    def test_new_user_create_credentials_and_login_invalid_name_highlight_and_message(self):
        pass

    def test_new_user_create_credentials_and_login_invalid_password_highlight_and_message(self):
        pass
 




# Create your tests here.
