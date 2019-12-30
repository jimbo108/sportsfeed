from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as web_driver_wait
from django.test import LiveServerTestCase
from django.contrib.auth.hashers import make_password
import time
from django.contrib.auth.models import User, UserManager

class SeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

 
    def wait_for_element(self, element_id, timeout=None):
        element_present = False
        if timeout is None:
            timeout = 1
        try:
            element_present = ec.presence_of_element_located((By.ID, element_id))
            web_driver_wait(self.browser, timeout).until(element_present)
        except TimeoutException as e:
            raise e

    def wait_for_elements(self, element_id_list, timeout=None):
        elements_present = False
        if timeout is None:
            timeout = 1

        for element_id in element_id_list:
            try:
                element_present = ec.presence_of_element_located((By.ID,
                                                                     element_id))
                web_driver_wait(self.browser, timeout).until(element_present)
            except TimeoutException as e:
                raise e
    


class NewVisitorLoginTest(SeleniumTest):

    def test_can_enter_email_and_password(self):
        self.browser.get(self.live_server_url + '/login/')

        self.wait_for_elements(['id_password', 'id_username'])

        username_input = self.browser.find_element_by_id('id_username')
        self.assertIsNotNone(username_input)

        username_input.send_keys('test_user')

        password_input = self.browser.find_element_by_id('id_password')
        self.assertIsNotNone(password_input)

        password_input.send_keys('password')

    def test_enter_credentials_failed_login_displays_failure_message(self):

        self.browser.get(self.live_server_url + '/login/')
        self.wait_for_elements(['id_password', 'id_username', 'login_submit_button'])

        username_input = self.browser.find_element_by_id('id_username')
        self.assertIsNotNone(username_input)

        username_input.send_keys('test@emailhost.com')

        password_input = self.browser.find_element_by_id('id_password')
        self.assertIsNotNone(password_input)

        password_input.send_keys('password')

        submit_button = self.browser.find_element_by_id('login_submit_button')
        self.assertIsNotNone(submit_button)

        submit_button.click()
        
        self.wait_for_element('failed_login_paragraph')

        failed_login_paragraph = self.browser.find_element_by_id('failed_login_paragraph')
        self.assertIsNotNone(failed_login_paragraph)

        failed_login_text = failed_login_paragraph.text

        self.assertEqual(failed_login_text, "Incorrect login credentials")

    def test_enter_credentials_successful_login_redirects_to_home(self):

        username = "test_username"
        password = "password"
        self.browser.get(self.live_server_url + '/login/')

        user = User.objects.create_user(username=username, password=password)
        #user_manager = UserManager()
        #user_manager.create_user(username, None, password)

        self.wait_for_elements(['id_password', 'id_username',
                                'login_submit_button'])

        username_input = self.browser.find_element_by_id('id_username')
        self.assertIsNotNone(username_input)

        username_input.send_keys(username)

        password_input = self.browser.find_element_by_id('id_password')
        self.assertIsNotNone(password_input)

        password_input.send_keys(password)

        submit_button = self.browser.find_element_by_id('login_submit_button')
        self.assertIsNotNone(submit_button)

        self.assertIsNotNone(User.objects.get(username=username))

        submit_button.click()

        time.sleep(1)
        
        self.assertEqual(self.browser.current_url, self.live_server_url + '/home/')

    # TODO: Figure out the 'expected str, bytes.. etc. error
    def test_new_user_create_credentials_and_login_redirects_to_preferences(self):

        username = "test_user"
        password = "test_pass_asdf"

        self.browser.get(self.live_server_url + '/login/')
        self.wait_for_element('new_user_link') 

        new_user_link = self.browser.find_element_by_id('new_user_link')
        self.assertIsNotNone(new_user_link)

        new_user_link.click()

        self.wait_for_elements(['id_username', 'id_password1',
                                'id_password2','new_user_submit_button'])


        self.assertEqual(self.browser.current_url, self.live_server_url + '/login/new/')

        username_input = self.browser.find_element_by_id('id_username')
        self.assertIsNotNone(username_input)

        username_input.send_keys(username)

        password_input = self.browser.find_element_by_id('id_password1')
        self.assertIsNotNone(password_input)

        password_input.send_keys(password)
        
        password_confirm_input = self.browser.find_element_by_id('id_password2')
        self.assertIsNotNone(password_confirm_input)

        password_confirm_input.send_keys(password)

        new_user_submit_button = self.browser.find_element_by_id('new_user_submit_button')
        self.assertIsNotNone(new_user_submit_button)

        new_user_submit_button.click()
        time.sleep(1)

        self.assertEqual(self.browser.current_url, self.live_server_url +
                         '/preferences/')

    def test_new_user_create_credentials_and_login_missing_fields_no_redirect(self):
        blank_username = ""
        password = "test_password_asdf"

        self.browser.get(self.live_server_url + '/login/')

        self.wait_for_element('new_user_link')

        new_user_link = self.browser.find_element_by_id('new_user_link')
        self.assertIsNotNone(new_user_link)

        new_user_link.click()
        time.sleep(1)

        self.assertEqual(self.browser.current_url, self.live_server_url + '/login/new/')

        self.wait_for_elements(['id_username', 'id_password1', 'id_password2',
                                'new_user_submit_button'])

        username_input = self.browser.find_element_by_id('id_username')
        self.assertIsNotNone(username_input)

        username_input.send_keys(blank_username)

        password_input = self.browser.find_element_by_id('id_password1')
        self.assertIsNotNone(password_input)

        password_input.send_keys(password)

        password_confirm_input = self.browser.find_element_by_id('id_password2')
        self.assertIsNotNone(password_confirm_input)

        password_confirm_input.send_keys(password)

        new_user_submit_button = self.browser.find_element_by_id('new_user_submit_button')
        self.assertIsNotNone(new_user_submit_button)

        new_user_submit_button.click()
        time.sleep(1)

        self.assertEqual(self.browser.current_url, self.live_server_url +
                         '/login/new/')

    def test_new_user_create_credentials_and_login_creates_user(self):

        username = "test_user"
        password = "test_pass_asdf"

        self.browser.get(self.live_server_url + '/login/')
        self.wait_for_element('new_user_link') 

        new_user_link = self.browser.find_element_by_id('new_user_link')
        self.assertIsNotNone(new_user_link)

        new_user_link.click()

        self.wait_for_elements(['id_username', 'id_password1',
                                'id_password2','new_user_submit_button'])


        self.assertEqual(self.browser.current_url, self.live_server_url + '/login/new/')

        username_input = self.browser.find_element_by_id('id_username')
        self.assertIsNotNone(username_input)

        username_input.send_keys(username)

        password_input = self.browser.find_element_by_id('id_password1')
        self.assertIsNotNone(password_input)

        password_input.send_keys(password)
        
        password_confirm_input = self.browser.find_element_by_id('id_password2')
        self.assertIsNotNone(password_confirm_input)

        password_confirm_input.send_keys(password)

        new_user_submit_button = self.browser.find_element_by_id('new_user_submit_button')
        self.assertIsNotNone(new_user_submit_button)

        new_user_submit_button.click()
        time.sleep(1)

        user = User.objects.get_by_natural_key(username)
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username, username)

    def test_new_user_create_credentials_and_login_duplicate_not_redirect(self):
        username = "test_user"
        password = "test_pass_asdf"

        User.objects.create_user(username, None, password)

        self.browser.get(self.live_server_url + '/login/')
        self.wait_for_element('new_user_link') 

        new_user_link = self.browser.find_element_by_id('new_user_link')
        self.assertIsNotNone(new_user_link)

        new_user_link.click()

        self.wait_for_elements(['id_username', 'id_password1',
                                'id_password2','new_user_submit_button'])


        self.assertEqual(self.browser.current_url, self.live_server_url + '/login/new/')

        username_input = self.browser.find_element_by_id('id_username')
        self.assertIsNotNone(username_input)

        username_input.send_keys(username)

        password_input = self.browser.find_element_by_id('id_password1')
        self.assertIsNotNone(password_input)

        password_input.send_keys(password)
        
        password_confirm_input = self.browser.find_element_by_id('id_password2')
        self.assertIsNotNone(password_confirm_input)

        password_confirm_input.send_keys(password)

        new_user_submit_button = self.browser.find_element_by_id('new_user_submit_button')
        self.assertIsNotNone(new_user_submit_button)

        new_user_submit_button.click()
        time.sleep(1)

        user = User.objects.get_by_natural_key(username)
        
        self.assertEqual(self.browser.current_url, self.live_server_url +
                         '/login/new/submit/')


       

class HomeViewTest(SeleniumTest):
    pass

class PreferencesViewTest(SeleniumTest):
    pass
#    def test_



# Create your tests here.
