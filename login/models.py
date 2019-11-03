from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class User(models.Model):
    email = models.EmailField(default='', primary_key=True)
    hashed_password = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200, default='')

    @classmethod
    def create_user(self, email, plain_text_password, name):
        hashed_password = make_password(plain_text_password)
        User.objects.create(email=email, hashed_password=hashed_password, name=name)
    
