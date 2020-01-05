from django import forms 
from home.models import Team
from .models import TeamPreference

class TeamPreferenceForm(forms.ModelForm):
    
    class Meta:
        model = TeamPreference
        fields = ['is_preference']

    def __init__(self, team_name, *args, **kwargs):
        super(TeamPreferenceForm, self).__init__(*args, **kwargs)
        self.fields['is_preference'].label = team_name
    
#    def __init__(self, user, *args, **kwargs):
#        super(TeamPreferenceForm, self).__init__(*args, **kwargs)
#
#        teams = Team.objects.all()
#        team_preferences = TeamPreference.objects.filter(user=user)
#       
#        teams_with_preferences = []
#
#        for team in teams:
#            if team_preferences.filter(team=team):
#                teams_with_preferences.append((team, True))
#            else:
#                teams_with_preferences.append((team, False))
#
#        for i, team_pref_tuple in enumerate(teams):
#            (team, preferred) = team_pref_tuple
#            self.fields['team_%s' % i] = forms.BooleanField(label=team.name,
#                                                            initial=preferred)
            
    
