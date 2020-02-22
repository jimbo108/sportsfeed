from django.test import TestCase
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User
from django.urls import resolve
from home.models import Team
from .models import TeamPreference
from .views import user_preferences
from .forms import TeamPreferenceForm


class PreferencesTest(TestCase):
    
    def test_preferences__get__returns_new_page(self):
        user = self.create_user()
        
        response = resolve('/user-preferences/' + str(user.id) + '/')
        self.assertEqual(response.func, user_preferences)
    
    def test_preferences__get__returns_correct_template(self):
        user = self.create_user()

        response = self.client.get('/user-preferences/' + str(user.id) + '/')
        self.assertTemplateUsed(response, 'user_preferences.html')
   
    def test_preferences__get__returns_correct_input_forms(self):
        user = self.create_user()
        team = self.create_team("team_0")
        num_unchecked = 4 

        team_preference = TeamPreference(user=user, team=team,
                                         is_preference=True)
        
        team_preference.save()
        for i in range(0,num_unchecked):
            self.create_team("team_" + str(i+1))

        response = self.client.get('/user-preferences/' + str(user.id) + '/')

        self.assertEqual(response.context['forms'][0].initial['is_preference'],
                         True)

        for i in range(1,num_unchecked+1):   
            self.assertNotIn('is_preference',
                             response.context['forms'][i].initial)

    # prefs for inactive teams marked as inactive
    # new active teams without prefs marked as active, not a preference
    # create a roster of a few teams, with a subset as preferences
    # save the preferences
    # mark the teams as inactive and add new active teams
    # GET
    # make sure the preferences are marked as inactive where appropriate and
    # that new ones have appeared
    def test_preferences__get__resets_prefs_correctly(self):
        user = self.create_user()
                
    def test_scratch_reset_user_teams(self):
        teams = []
        user = self.create_user()
        for i in range(0,4):
            teams.append(self.create_team("test_team" + str(i)))
        teams.append(self.create_team("test_team" + str(4), False))
        active_teams = Team.get_active_teams()

        self.create_preference(user, teams[0])
        self.create_preference(user, teams[4])

        TeamPreference.reset_user_teams(user, active_teams)
#    def test_preferences__post__sets_correct_state(self):
#        user = self.create_user()
#        team = self.create_team("team_0")
#
#        for i in range
    
    @staticmethod
    def create_preference(user: User, team: Team) -> TeamPreference:
        pref = TeamPreference(user=user, team=team)
        pref.save()
        return pref

    @staticmethod
    def create_user() -> User:
        username = "test_username"
        password = "test_password_asdf"

        user = User(id=1, username=username, password=password)
        user.save()

        return user

    @staticmethod
    def create_team(team_name: str="test_team", is_active: bool=True) -> Team:
        team = Team(name=team_name, is_active=is_active)
        team.save()

        return team

