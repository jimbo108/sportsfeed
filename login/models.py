from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
#from home.models import
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    

