from django.db import models
from enum import Enum

class Team(models.Model):
    name = models.CharField(max_length=100)

class Api(models.Model):
    name = models.CharField(max_length=100)
 
class TeamMapping(models.Model):
    team = models.ForeignKey(Team, on_delete=models.deletion.CASCADE)
    api = models.ForeignKey(Api, on_delete=models.deletion.CASCADE)
    numeric_external_identifier = models.IntegerField()
    string_external_idenifier = models.CharField(max_length=100)

      

   

