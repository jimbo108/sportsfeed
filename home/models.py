from django.db import models
from .enums import ExternalIdentifierType
from typing import Union

class Team(models.Model):
    name = models.CharField(max_length=100) 
    is_active = models.BooleanField(default=True)
    
    @classmethod
    def get_active_teams(self):
        return Team.objects.filter(is_active=True)

class Api(models.Model):
    name = models.CharField(max_length=100)
 
class TeamMapping(models.Model):
    team = models.ForeignKey(Team, on_delete=models.deletion.CASCADE)
    api = models.ForeignKey(Api, on_delete=models.deletion.CASCADE)
    numeric_external_identifier = models.IntegerField(default=None, null=True)
    string_external_identifier = models.CharField(max_length=100, default=None,
                                                null=True)
    
    @classmethod
    def get_team_from_external_id(self, external_identifier_type:
                                  ExternalIdentifierType, external_identifier:
                                  Union[int, str], api_id: int):
        team = None
        team_mapping = None

        try: 
            api = Api.objects.get(id=api_id)
        except Api.DoesNotExist:
            return None
        
        try:
            if external_identifier_type == ExternalIdentifierType.NUMERIC:
                team_mapping = self.objects.get(api=api,
                                                       numeric_external_identifier=external_identifier)
            elif external_identifier_type == ExternalIdentifierType.STRING:
                team_mapping = self.objects.get(api=api,
                                                       string_external_identifier=external_identifier)
            else:
                raise ValueError("Invalid ExternalIdentifierType enum") 
        except self.DoesNotExist:
            return None
        except self.MultipleObjectsReturned as e:
            raise e
        if not team_mapping:
            return None

        return team_mapping.team
             
      

   

