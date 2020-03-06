from typing import List
from django.db import models
from django.contrib.auth.models import User
from home.models import Team

class TeamPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.deletion.CASCADE)
    is_preference = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) 

    @classmethod
    def get_user_team_preferences(self, user: User):
        # Calling reset_user_teams on every get is not very efficient, but no
        # reason to change it at the moment.  Potential future enhancement to
        # track active team changes
        
        current_active_teams = Team.get_active_teams()
        self.reset_user_teams(user, current_active_teams)
        return self._get_user_team_preferences(user)
   
    @classmethod
    def _get_user_team_preferences(self, user:User):
        return self.objects.filter(user=user, is_active=True)

    @classmethod
    def create_new_active_teams(self, user: User):
        pass 
    
    # Bookmark -- write tests and add to view
    @classmethod
    def reset_user_teams(self, user: User, active_teams: List[Team]) -> None:
        user_team_prefs = self._get_user_team_preferences(user)
        teams_without_prefs = list(set(active_teams) - set([pref.team for pref in
                                                            user_team_prefs]))

        new_inactive_prefs = [pref for pref in filter(lambda x: not x.team.is_active,
                                                      user_team_prefs)]
        
        new_prefs = list(map(lambda x: TeamPreference(user=user, team=x),
                        teams_without_prefs))
        
        for pref in new_prefs:
            pref.save()
        
        for pref in new_inactive_prefs:
            pref.is_active = False
            pref.save()


                                        
       
