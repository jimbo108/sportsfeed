from django.test import TestCase
from django.urls import resolve
from login.views import login, submit, new_user
from login.models import User
from django.contrib.auth.hashers import make_password

class LoginTest(TestCase):

    def test_login_returns_new_page(self):
        response = resolve('/login/')
        self.assertEqual(response.func, login)
    
    def test_login_returns_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'login.html')
       
    def test_login_submit_redirects_to_home_on_success(self):
        email="test@testhost.com" 
        password="password"

        User.objects.create(email=email, hashed_password=make_password(password))

        response = self.client.post('/login/submit/', data={'email': email, 'password': password})

        self.assertRedirects(response, '/home/')

    def test_login_submit_sets_failure_context_on_failure(self):
        incorrect_email="incorrect@testhost.com"
        email = "test@testhost.com"
        password="password"

        User.objects.create(email=email, hashed_password=make_password(password))

        response = self.client.post('/login/submit/', data={'email': incorrect_email, 'password': password})

        self.assertTrue(response.context.get('failure'))

class NewUserTest(TestCase):

    def test_new_user_returns_correct_view(self):
        response = resolve('/login/new/')
        self.assertEqual(response.func, new_user)
    
    def test_new_user_renders_correct_template(self):
        response = self.client.get('/login/new/')
        self.assertTemplateUsed(response, 'new_user.html')

    def test_new_user_submit_sets_failure_context_on_invalid_email(self):
        name = "Test Testington"
        invalid_email = "invalidEmail"
        password = "password"
        data = {'name': name, 'email': invalid_email, 'password': password}

        response = self.client.post('/login/new/submit/', data)

        self.assertTrue(response.context.get('invalid_email'))

    def test_new_user_submit_sets_failure_context_on_overshort_password(self):
        name = "Test Testington"
        email = "test@testhost.com"
        overshort_password = "pass"
        data = {'name': name, 'email': email, 'password': overshort_password}

        response = self.client.post('/login/new/submit/', data)

        self.assertTrue(response.context.get('overshort_password'))

    def test_new_user_submit_sets_failure_context_on_missing_name(self):
        blank_name = ""
        email = "test@testhost.com"
        password = "password"
        data = {'name': blank_name, 'email': email, 'password': password}

        response = self.client.post('/login/new/submit/', data)

        self.assertTrue(response.context.get('missing_name'))

    def test_new_user_submit_sets_failure_context_on_missing_email(self):
        name = "Test Testington"
        blank_email = ""
        password = "password"
        data = {'name': name, 'email': blank_email, 'password': password}

        response = self.client.post('/login/new/submit/', data)

        self.assertTrue(response.context.get('missing_email'))

    def test_new_user_submit_sets_failure_context_on_missing_password(self):
        name = "Test Testington"
        email = "test@testhost.com"
        blank_password = "" 

        data = {'name': name, 'email': email, 'password': blank_password}

        response = self.client.post('/login/new/submit/', data)
       
        self.assertTrue(response.context.get('missing_password'))



    def test_new_user_submit_sets_failure_context_on_invalid_name(self):
        invalid_name = "Test Testington1"
        email = "test@testhost.com"
        password = "password"
        data = {'name': invalid_name, 'email': email, 'password': password}

        response = self.client.post('/login/new/submit/', data)

        self.assertTrue(response.context.get('invalid_name'))

    def test_new_user_submit_redirects_to_home_on_success(self):
        name = "Test Testington"
        email = "test@testhost.com"
        password = "password"
        data = {'name': name, 'email': email, 'password': password}

        response = self.client.post('/login/new/submit/', data)

        self.assertRedirects(response, '/home/')
    
    def test_new_user_submit_creates_user_on_success(self):
        name = "Test Testington"
        email = "test@testhost.com"
        password = "password"
        data = {'name': name, 'email': email, 'password': password}

        self.client.post('/login/new/submit/', data)

        failed_to_find_user = False
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            failed_to_find_user = True
        
        self.assertFalse(failed_to_find_user)
        self.assertIsNotNone(user)
        self.assertEqual(type(user), User) 


    def test_new_user_submit_does_not_create_user_on_failure(self):
        name = "Test Testington"
        email = "test@testhost.com"
        blank_password = ""
        data = {'name': name, 'email': email, 'password': blank_password}

        self.client.post('/login/new/submit/', data)

        failed_to_find_user = False
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            failed_to_find_user = True
        self.assertTrue(failed_to_find_user) 
    
    def test_new_user_submit_does_not_create_user_on_duplicate_email(self):
        name = "Test Testington"
        email = "test@testhost.com"
        password = "password"
        data = {'name': name, 'email': email, 'password': password}

        response = self.client.post('/login/new/submit/', data)

        failed_to_find_user = False
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            failed_to_find_user = True
        
        self.assertFalse(failed_to_find_user)
        self.assertIsNotNone(user)
        self.assertEqual(type(user), User) 

        different_password="password_two"
        different_name = "Test Testington Jr"
        data = {'name': different_name, 'email': email, 'password': different_password}

        response = self.client.post('/login/new/submit/', data)

        self.assertTrue(response.context.get('duplicate_email'))
    
#    def test_new_user_register_preferences_returns_template(self):
#        response = self.client.get()

#class UserModelTest(TestCase):


# Create your tests here.
