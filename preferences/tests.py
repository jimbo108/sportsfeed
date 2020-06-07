"""Tests for the Preferences app."""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import resolve
from home.models import Team
from Preferences import models, views

# pylint: disable=missing-class-docstring,missing-function-docstring
class PreferencesTest(TestCase):

    def test_preferences__get__returns_new_page(self):
        user = self.create_user()

        response = resolve('/user-preferences/' + str(user.id) + '/')
        self.assertEqual(response.func, views.user_preferences)

    def test_preferences__get__returns_correct_template(self):
        user = self.create_user()

        response = self.client.get('/user-preferences/' + str(user.id) + '/')
        self.assertTemplateUsed(response, 'user_preferences.html')

    def test_preferences__get__returns_correct_input_forms(self):
        user = self.create_user()
        team = self.create_team("team_0")
        num_unchecked = 4

        team_preference = models.TeamPreference(user=user, team=team,
                                                is_preference=True)

        team_preference.save()
        for i in range(0, num_unchecked):
            self.create_team("team_" + str(i+1))

        response = self.client.get('/user-preferences/' + str(user.id) + '/')

        self.assertEqual(response.context['forms'][0].initial['is_preference'],
                         True)

        for i in range(1, num_unchecked+1):
            self.assertNotIn('is_preference',
                             response.context['forms'][i].initial)

    # prefs for inactive teams marked as inactive
    # new active teams without prefs marked as active, not a preference
    # create a roster of a few teams, with a subset as preferences (user, team,
    # preference)
    # save the preferences
    # mark the teams as inactive and add new active teams
    # GET
    # make sure the preferences are marked as inactive where appropriate and
    # that new ones have appeared
    def test_preferences__get__resets_prefs_correctly(self):
        user = self.create_user()
        found_inactive_team = False
        found_new_active_team = False
        teams = []

        for i in range(0, 5):
            teams.append(self.create_team(team_name="test_team" + str(i)))

        self.create_preference(user, teams[0])
        self.create_preference(user, teams[1])

        response = self.client.get('/user-preferences/' + str(user.id) + '/')
        forms = response.context['forms']

        for i in range(0, 2):
            self.assertTrue(forms[i].initial['is_preference'])

        teams[0].is_active = False
        teams[0].save()

        teams.append(self.create_team(team_name="test_team5"))

        response = self.client.get('/user-preferences/' + str(user.id) + '/')
        forms = response.context['forms']

        for form in forms:
            form_label = form.fields['is_preference'].label
            if form_label == 'test_team0':
                found_inactive_team = True
            elif form_label == 'test_team1':
                self.assertTrue(form.initial['is_preference'])
            elif form_label == 'test_team5':
                found_new_active_team = True

        self.assertFalse(found_inactive_team)
        self.assertTrue(found_new_active_team)

    def test_preferences__post__sets_correct_state(self):
        teams = []

        for i in range(0, 5):
            teams.append(self.create_team(team_name="test_team" + str(i)))

#        self.client.post('/user-preferences/' + str(user.id) + '/', data={


    @staticmethod
    def create_preference(user: User, team: Team) -> models.TeamPreference:
        pref = models.TeamPreference(user=user, team=team)
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
    def create_team(team_name: str="test_team", is_active: bool=True) -> Team: #pylint: disable=C0326
        team = Team(name=team_name, is_active=is_active)
        team.save()

        return team
