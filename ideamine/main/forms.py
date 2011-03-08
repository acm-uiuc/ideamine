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

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
