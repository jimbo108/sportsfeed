from typing import List
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from home.models import Team
from django.contrib.auth.models import User
from .models import TeamPreference
from .forms import TeamPreferenceForm

def user_preferences(request: HttpRequest, user_id: int) -> HttpResponse:
    user = User.objects.get(id=user_id)
    if user is None:
        return HttpResponse(status=500)

    if request.method == "POST":
        pass
    else:
        active_teams = Team.get_active_teams()
        team_preferences = TeamPreference.get_user_team_preferences(user)
        preference_forms = get_preference_forms(team_preferences, active_teams)

        return render(request, 'user_preferences.html', context={'forms': preference_forms})
                                                

def get_preference_forms(team_preferences: List[TeamPreference],
                         active_teams: List[Team]) -> List[TeamPreferenceForm]:
    preference_forms = []

    for team in active_teams:
        pref = None
        pref_form = None
        try:
            pref = team_preferences.get(team=team)
        except TeamPreference.DoesNotExist:
            pass

        if pref is not None:
            pref_form = TeamPreferenceForm(team_name=team.name, instance=pref)
        else:
            pref_form = TeamPreferenceForm(team_name=team.name)

        preference_forms.append(pref_form)

    return preference_forms
