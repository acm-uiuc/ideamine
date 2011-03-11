from django import forms
from django.forms import ModelForm, Form
from main.models import *

class IdeaForm(ModelForm):
    tags_field = forms.CharField(label='Tags', required=False)

    class Meta:
        model = Idea
        fields = ('short_name', 'desc')

class TagForm(ModelForm):
    class Meta:
        model = Tag

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ImageUploadForm(ModelForm):
    class Meta:
        model = Image
        exclude = ('idea', 'uploader')

class UserConfirmForm(Form):
    user_pk = forms.ModelChoiceField(queryset=UserProfile.objects.all())

def generate_idea_form(idea, data=None):
    tag_string = idea.tags_to_s()

    form_data = dict(tags_field=tag_string, short_name=idea.short_name, desc=idea.desc)
    if data:
        form_data = data
    return IdeaForm(form_data, instance=idea)
