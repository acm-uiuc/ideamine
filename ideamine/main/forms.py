from django.forms import ModelForm
from main.models import *

class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        exclude = ('owner', 'members',)
