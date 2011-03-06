from django import forms
from django.forms import ModelForm
from main.models import *

class IdeaForm(ModelForm):
    tags = forms.CharField(label='Tags', required=False)

    class Meta:
        model = Idea
        exclude = ('owner', 'members',)

class TagForm(ModelForm):
    class Meta:
        model = Tag
