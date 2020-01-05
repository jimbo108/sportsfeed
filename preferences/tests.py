from django.test import TestCase
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
        team_preference = TeamPreference(user=user, team=team)
        
        for i in range(0,num_unchecked):
            self.create_team("team_" + str(i+1))

        response = self.client.get('/user-preferences/' + str(user.id))

        self.assertEqual(response.context['forms'][0].initial['is_preference'],
                         True)

        for i in range(0,num_unchecked):   
            self.assertEqual(response.context['forms'][i].initial['is_preference'],
                             False)       
    
    @staticmethod
    def create_user() -> User:
        username = "test_username"
        password = "test_password_asdf"

        user = User(id=1, username=username, password=password)
        user.save()

        return user

    @staticmethod
    def create_team(team_name: str="test_team") -> Team:
        team = Team(name=team_name)
        team.save()

        return team

