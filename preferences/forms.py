from django import forms 
from home.models import Team
from .models import TeamPreference
from django.forms import formset_factory
from django.forms.models import modelformset_factory

class TeamPreferenceForm(forms.ModelForm):
    
    class Meta:
        model = TeamPreference
        fields = ['is_preference']

    def __init__(self, *args, **kwargs):
        super(TeamPreferenceForm, self).__init__(*args, **kwargs) 
        self.fields['is_preference'].label = self.instance.team.name

TeamPreferenceFormSet = modelformset_factory(TeamPreference, 
                                             form=TeamPreferenceForm, extra=0)
                                            
   
