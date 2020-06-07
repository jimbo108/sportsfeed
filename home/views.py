from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from preferences import models as preference_models
from home import models
from home import services

@csrf_exempt
def home(request):
    """View for generating the feed.

    Gets all fixtures for a user based on team preferences.
    """
    fixtures = set()
    # Get user
    user = request.user

    if not refresh_fixtures():
        # TODO: logging
        pass

    # Pull preferences
    preferred_teams = preference_models.TeamPreference.get_user_preferred_teams(user)
    if preferred_teams is None:
        preferred_teams = models.Team.objects.filter(is_active=True)

    # TODO: Handle Game Weeks
    for team in preferred_teams:
        fixtures_for_team = models.Fixture.objects.filter(Q(home_team=team) | Q(away_team=team))
        fixtures = fixtures.union(set(fixtures_for_team))

    fixtures = sorted(fixtures, reverse=True,
                      key=lambda x: x.kickoff_time_utc.timestamp())
    return render(request, 'home/home.html', context={'fixtures': fixtures})


def refresh_fixtures() -> bool:  # pylint: disable=missing-function-docstring
    return services.FDDOApiClient().request()
