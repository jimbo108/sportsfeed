from typing import List
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from home.models import Team
from django.contrib.auth.models import User
from .models import TeamPreference
from .forms import TeamPreferenceFormSet


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
                                                
 
