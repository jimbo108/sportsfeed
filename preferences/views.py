from typing import List
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from home.models import Team
from django.contrib.auth.models import User
from .models import TeamPreference
from .forms import TeamPreferenceForm, TeamPreferenceFormSet

def user_preferences(request: HttpRequest, user_id: int) -> HttpResponse:
    user = User.objects.get(id=user_id)
    if user is None:
        return HttpResponse(status=500)

    if request.method == "POST":
        formset = TeamPreferenceFormSet(request.POST)
        if formset.is_valid():
            formset.save()
        return redirect('/home/') 
    else: 
        active_teams = Team.get_active_teams()
        TeamPreference.reset_user_teams(user, active_teams)
        formset = TeamPreferenceFormSet(queryset=TeamPreference.objects.filter(user=user,
                                                                               is_active=True))
        return render(request, 'user_preferences.html', context={'formset':
                                                                 formset,
                                                                 'user_id':
                                                                  user.id})
                                                
#def user_preferences(request: HttpRequest, user_id: int) -> HttpResponse:
#    user = User.objects.get(id=user_id)
#    if user is None:
#        return HttpResponse(status=500)
#
#    if request.method == "POST":
#        breakpoint()
#        pass
#    else:
#        active_teams = Team.get_active_teams()
#        team_preferences = TeamPreference.get_user_team_preferences(user)
#        preference_forms = get_preference_forms(team_preferences, active_teams)
#        return render(request, 'user_preferences.html', context={'forms':
#                                                                 preference_forms,
#                                                                 'user_id':
#                                                                  user.id})
# 
def get_preference_formset(user: User) -> TeamPreferenceFormSet:
    active_teams = Team.get_active_teams()
 
    preference_forms = []
    
    for team in active_teams:
        pref = None
        pref_form = None
        try:
            pref = team_preferences.get(team=team)
        except TeamPreference.DoesNotExist:
            pass

        if pref is not None:
            pref_form = TeamPreferenceForm(team_name=team.name, instance=pref,
                                           initial={'is_preference': True})
        else:
            pref_form = TeamPreferenceForm(team_name=team.name)

        preference_forms.append(pref_form)

    return preference_forms

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
            pref_form = TeamPreferenceForm(team_name=team.name, instance=pref,
                                           initial={'is_preference': True})
        else:
            pref_form = TeamPreferenceForm(team_name=team.name)

        preference_forms.append(pref_form)

    return preference_forms
