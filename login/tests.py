from django.test import TestCase
from django.urls import resolve
from login.views import login_user, login_submit, new_user
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginTest(TestCase):

    def test_login_returns_new_page(self):
        response = resolve('/login/')
        self.assertEqual(response.func, login_user)
    
    def test_login_returns_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'login.html')
       
class NewUserTest(TestCase):

    def test_new_user_returns_correct_view(self):
        response = resolve('/login/new/')
        self.assertEqual(response.func, new_user)
    
    def test_new_user_renders_correct_template(self):
        response = self.client.get('/login/new/')
        self.assertTemplateUsed(response, 'new_user.html')

   
   
#    def test_new_user_register_preferences_returns_template(self):
#        response = self.client.get()

#class UserModelTest(TestCase):


# Create your tests here.
