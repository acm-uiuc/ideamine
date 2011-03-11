from django import forms
from django.forms import ModelForm
from django.forms import Form
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

class IdeaUpdateForm(ModelForm):
    class Meta:
        model = Idea
        fields = ('desc', 'short_name', 'tags')

class ImageUploadForm(ModelForm):
    class Meta:
        model = Image
        exclude = ('idea', 'uploader')

class UserConfirmForm(Form):
    user_pk = forms.ModelChoiceField(queryset=UserProfile.objects.all())
