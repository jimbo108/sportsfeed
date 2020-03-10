from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class LoginForm(AuthenticationForm):
    pass


class NewUserForm(UserCreationForm):
    error_css_class = 'form-error'



