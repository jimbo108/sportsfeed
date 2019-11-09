from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
#from home.models import
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    email = models.EmailField(default='', primary_key=True)
    hashed_password = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200, default='')

    @classmethod
    def create_user(self, email, plain_text_password, name):
        hashed_password = make_password(plain_text_password)
        User.objects.create(email=email, hashed_password=hashed_password, name=name)

#class UserPreferences(models.Model):
#    league = models.C