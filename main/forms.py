from django import forms
from django.forms import ModelForm, Form
from main.models import *

class IdeaForm(ModelForm):
    tags_field = forms.CharField(label='Tags', required=False)

    class Meta:
        model = Idea
        fields = ('short_name', 'desc', 'website')

class IdeaUpdateForm(IdeaForm):
    class Meta:
        model = Idea
        fields = ('short_name', 'desc', 'website', 'progress')

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

def generate_idea_form(FormType, idea, data=None):
    tag_string = None
    if idea.pk:
        tag_string = idea.tags_to_s()

    form_data = dict(tags_field=tag_string, short_name=idea.short_name, desc=idea.desc, progress=idea.progress, website=idea.website)
    if data:
        form_data = data
    return FormType(form_data, instance=idea)
