from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from preferences.models import TeamPreference
from .models import Fixture, Team
from .services import FDDOApiClient

@csrf_exempt
def home(request):
    fixtures = set()
    # Get user
    user = request.user

    if not refresh_fixtures():
        # TODO: logging
        pass

    # Pull preferences
    preferred_teams = TeamPreference.get_user_preferred_teams(user)
    if preferred_teams is None:
        preferred_teams = Team.objects.filter(is_active=True)

    # TODO: Handle seasons
    for team in preferred_teams:
        fixtures_for_team = Fixture.objects.filter(Q(home_team=team) | Q(away_team=team))
        fixtures = fixtures.union(set(fixtures_for_team))

    # DEBUG:
    for fixture in fixtures:
        print(fixture.__dict__)
    
    fixtures = sorted(fixtures, reverse=True,
                                key=lambda x: x.kickoff_time_utc.timestamp())
    return render(request, 'home/home.html', context={'fixtures': fixtures})


def refresh_fixtures() -> bool:
    return FDDOApiClient().request()
