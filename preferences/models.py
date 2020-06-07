"""Defines models for the home feed.

Also contains some class methods for interacting with Team rows.
"""
from typing import List
from django.db import models
from django.contrib.auth.models import User
from home.models import Team

class TeamPreference(models.Model):
    """Model representing a team preference.

    Also contains public methods for interacting with team_preferences.

    Attributes:
        user::ForeignKey (User)
            The user the preference is associated with.
        team::ForeignKey (Team)
            The preferred or unpreferred Team.
        is_preference::BooleanField
            Whether or not the user prefers this team.
        is_active::BooleanField
            Whether this is an active preference
    """
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.deletion.CASCADE)
    is_preference = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_user_preferred_teams(cls, user: User):
        """Returns the team the entered user prefers.

        Args:
            user::User
                The user to get preferred teams for.

        Returns:
            The Team models for active Teams that are preferences.
        """
        preferred_prefs = cls.objects.filter(user=user, is_active=True, is_preference=True)
        teams = [pref.team for pref in preferred_prefs]
        return teams

    @classmethod
    def _get_user_team_preferences(cls, user: User):
        """Get all TeamPreferences (whether preferred or not) for the user.

        Args:
            user::User
               The user to return TeamPreferences for.

        Returns:
            TeamPreferences associated with the user and active teams.
        """
        return cls.objects.filter(user=user, is_active=True)

    # Bookmark -- write tests and add to view
    @classmethod
    def reset_user_teams(cls, user: User, active_teams: List[Team]) -> None:
        """Resets the user team preferences based on active Teams

        Args:
            user::User
                The user to reset teams for.
            active_teams::Team
                A list of active teams, pre-retrieved.
        """
        user_team_prefs = cls._get_user_team_preferences(user)
        teams_without_prefs = list(set(active_teams) - {pref.team for pref in user_team_prefs})

        new_inactive_prefs = list(filter(lambda x: not x.team.is_active,
                                         user_team_prefs))

        new_prefs = list(map(lambda x: TeamPreference(user=user, team=x),
                             teams_without_prefs))

        for pref in new_prefs:
            pref.save()

        for pref in new_inactive_prefs:
            pref.is_active = False
            pref.save()

