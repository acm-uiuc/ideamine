# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core import serializers
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import list_detail

from main.forms import *
from main.models import *

import main.signals
import json

def index(request):
    c = RequestContext(request, {})
    return render_to_response("index.html", c)

def user_create(request, *args, **kwargs):
    if request.method == 'POST':
        new_user = User()
        user_form = UserCreationForm(request.POST, instance=new_user)
        if user_form.is_valid():
            user_form.save()
            new_user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, new_user)
            redirect_to = new_user.get_profile().get_absolute_url()
            return HttpResponseRedirect(redirect_to)
    else:
        user_form = UserCreationForm()

    kwargs.update(csrf(request))
    c = RequestContext(request, dict(form=user_form, **kwargs))
    return render_to_response('auth/user_form.html', c)

@login_required
def user_detail(request, object_id, **kwargs):
    update_user = get_object_or_404(User, pk=object_id)
    request_profile = request.user.get_profile()
    if request_profile.can_update_user(update_user):
        user_form = UserUpdateForm(instance=update_user)
        kwargs['form'] = user_form

    kwargs.update(csrf(request))
    c = RequestContext(request, dict(object=update_user, **kwargs))
    return render_to_response('auth/user_detail.html', c)

@login_required
def user_update(request, object_id, **kwargs):
    update_user = get_object_or_404(User, pk=object_id)
    request_profile = request.user.get_profile()
    if not request_profile.can_update_user(update_user):
        return HttpResponseForbidden()

    redirect_to = update_user.get_profile().get_absolute_url()
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=update_user)
        if user_update_form.is_valid():
            user_update_form.save()
            return HttpResponseRedirect(redirect_to)
    return HttpResponseRedirect(redirect_to)

@login_required
def redirect_to_user(request, *args, **kwargs):
    redirect_to = request.user.get_profile().get_absolute_url()
    return HttpResponseRedirect(redirect_to)

@login_required
def idea_create(request, *args, **kwargs):
    if request.method == 'POST':
        idea = Idea(owner=request.user.get_profile())
        idea_form = generate_idea_form(IdeaForm, idea, request.POST)
        if idea_form.is_valid():
            idea_form.save()
            idea.change_tags(idea_form.cleaned_data['tags_field'])
            redirect_to = idea.get_absolute_url()
            return HttpResponseRedirect(redirect_to)
    else:
        idea_form = IdeaForm()

    kwargs.update(csrf(request))
    c = RequestContext(request, dict(form=idea_form, **kwargs))
    return render_to_response('main/idea_form.html', c)

@login_required
def idea_detail(request, object_id, **kwargs):
    update_idea = get_object_or_404(Idea, pk=object_id)
    request_profile = request.user.get_profile()
    if update_idea.can_destroy(request.user):
        kwargs['can_delete'] = True
    if request.method == 'POST':
        if request_profile.can_update_idea(update_idea):
            idea_form = generate_idea_form(IdeaUpdateForm, update_idea, request.POST)
            kwargs['form'] = idea_form
            if idea_form.is_valid():
                idea_form.save()
                redirect_to = update_idea.get_absolute_url()
                return HttpResponseRedirect(redirect_to)
        else:
            return HttpResponseForbidden()
    else:
        if request_profile.can_update_idea(update_idea):
            idea_form = generate_idea_form(IdeaUpdateForm, update_idea)
            kwargs['form'] = idea_form

    kwargs.update(csrf(request))
    c = RequestContext(request, dict(object=update_idea, **kwargs))
    return render_to_response('main/idea_detail.html', c)

@login_required
def idea_update(request, object_id, **kwargs):
    update_idea = get_object_or_404(Idea, pk=object_id)
    if not request.user.get_profile().can_update_idea(update_idea):
        return HttpResponseForbidden()
    if request.method == 'POST':
        idea_update_form = generate_idea_form(IdeaUpdateForm, update_idea, request.POST)
        if idea_update_form.is_valid():
            idea_update_form.save()
            update_idea.change_tags(idea_update_form.cleaned_data['tags_field'])
            redirect_to = update_idea.get_absolute_url()
            return HttpResponseRedirect(redirect_to)
    else:
        c = RequestContext(request, {"shortmsg":"Request Error",
            "msg":"Method incorrectly called with get"})
        return render_to_response('notifications/notify.html', c)

@login_required
def idea_join(request, object_id, *args, **kwargs):
    if request.method == "POST":
        idea = get_object_or_404(Idea, pk=object_id)
        if idea.is_member(request.user) or idea.is_owner(request.user):
            c = RequestContext(request, {"shortmsg":"Error",
                "msg":"You are already a member of this project."})
            return render_to_response('notifications/notify.html', c)

        idea.add_member(request.user)
        redirect_to = idea.get_absolute_url()
        return HttpResponseRedirect(redirect_to)
    else:
        c = RequestContext(request, {"shortmsg":"Request Error",
            "msg":"Method incorrectly called with get"})
        return render_to_response('notifications/notify.html', c)

@login_required
def idea_leave(request, object_id, *args, **kwargs):
    if request.method == "POST":
        idea = get_object_or_404(Idea, pk=object_id)
        if idea.is_member(request.user):
            idea.remove_member(request.user)
            redirect_to = idea.get_absolute_url()
            return HttpResponseRedirect(redirect_to)

        c = RequestContext(request, {"shortmsg":"Error",
            "msg":"You are not a member of this project."})
        return render_to_response('notifications/notify.html', c)
    else:
        c = RequestContext(request, {"shortmsg":"Request Error",
            "msg":"Method incorrectly called with get"})
        return render_to_response('notifications/notify.html', c)

@login_required
def idea_destroy(request, object_id, *kwargs):
    if request.method == 'POST':
        idea = get_object_or_404(Idea, pk=object_id)
        if idea.can_destroy(request.user):
            idea.delete()
            c = RequestContext(request, {"shortmsg":"Idea Deleted",
                "msg":"Idea successfully deleted."})
            return render_to_response('notifications/notify.html', c)
        else:
            return HttpResponseForbidden()
    else:
        c = RequestContext(request, {"shortmsg":"Request Error",
            "msg":"Method incorrectly called with get"})
        return render_to_response('notifications/notify.html', c)

@login_required
def confirm_member(request, object_id, *args, **kwargs):
    if request.method == "POST":
        idea = get_object_or_404(Idea, pk=object_id)
        if idea.can_edit(request.user):
            form = UserConfirmForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user_pk']
                if idea.is_member(user.user):
                    if not idea.is_confirmed(user.user):
                        idea.confirm_member(user.user)
                    else:
                        c = RequestContext(request, {"shortmsg":"Error",
                            "msg":"This user is already a confirmed member."})
                        return render_to_response('notifications/notify.html', c)
                else:
                    c = RequestContext(request, {"shortmsg":"Error",
                        "msg":"This user is not a member of this project"})
                    return render_to_response('notifications/notify.html', c)
        else:
            return HttpResponseForbidden()
    else:
        c = RequestContext(request, {"shortmsg":"Request Error",
            "msg":"Method incorrectly called with get"})
        return render_to_response('notifications/notify.html', c)

    redirect_to = idea.get_absolute_url()
    return HttpResponseRedirect(redirect_to)

def tag_suggest(request, **kwargs):
    response = HttpResponse(mimetype="text/json")
    search = request.GET['search']
    tags = Tag.objects.filter(name__istartswith=search)
    response_list = []

    for tag in tags:
        response_list.append([tag.name, tag.name])

    response.content = json.dumps(response_list)
    return response

@login_required
def image_upload(request, object_id, *args, **kwargs):
    if request.method == "POST":
        idea = get_object_or_404(Idea, pk=object_id)
        new_image = Image(idea=idea, uploader=request.user.get_profile())
        upload_form = ImageUploadForm(request.POST, request.FILES, instance=new_image)
        if upload_form.is_valid():
            upload_form.save()
            return HttpResponseRedirect(idea.get_absolute_url())
    else:
        upload_form = ImageUploadForm()

    kwargs.update(csrf(request))
    c = RequestContext(request, dict(form=upload_form, **kwargs))
    return render_to_response('main/image_form.html', c)
