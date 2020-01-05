from django.test import TestCase
from django.contrib.auth import User
from home.models import Team
from .models import TeamPreference
from .views import user_preferences
from .forms import TeamPreferenceForm

class PreferencesTest(TestCase):
    
    def test_preferences__get__returns_new_page(self):
        user = self.create_user()
        
        response = resolve('/user-preferences/' + str(user.id))
        self.assertEqual(response.func, user_preferences)
    
    def test_preferences__get__returns_correct_template(self):
        user = self.create_user()
        response = self.client.get('/user-preferences/' + str(user.id))

        self.assertTemplateUsed(response, 'user_preferences.html')
    
    def test_preferences_model__instantiate_field__contains_correct_fields(self):
        user = self.create_user()
        team = self.create_team("team_1")
        
        team_preference = TeamPreference(user=user, team=team)

        for i in range(0,10):
            self.create_team("team_" + str(i+2))
        #preferences_model = TeamPreferenceForm(
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

