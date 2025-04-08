from django import forms
from .models import Lives,Works

class LivesForm(forms.ModelForm):
    class Meta:
        model = Lives
        fields = ['name','street','city']

class WorksForm(forms.ModelForm):
    class Meta:
        model = Works
        
        fields = ['name','company','salary']