from django.db import models
from django.contrib.auth.models import User
from home.models import Team

class TeamPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.deletion.CASCADE)
    is_preference = models.BooleanField(default=False)
    
    @classmethod
    def get_user_team_preferences(self, user: User):
        return TeamPreference.objects.filter(user=user) 
