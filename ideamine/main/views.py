# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core import serializers
from django.db.models.signals import post_save
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import list_detail

from main.forms import *
from main.models import *

def index(request):
    c = RequestContext(request, {})
    return render_to_response("index.html", c)

def members(request, object_id=None):
    if not object_id:
        raise Http404
    return render_to_response("users.html",
        { 'object_list' : Idea.objects.get(id=object_id).members.all(),
          'h1' : 'members' })

def user_create(request, *args, **kwargs):
    if request.method == 'POST':
        new_user = User()
        user_form = UserCreationForm(request.POST, instance=new_user)
        if user_form.is_valid():
            user_form.save()
            new_user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, new_user)
            redirect_to = '/users/self'
            return HttpResponseRedirect(redirect_to)
    else:
        user_form = UserCreationForm()

    kwargs.update(csrf(request))
    c = RequestContext(request, dict(form=user_form, **kwargs))
    return render_to_response('auth/user_form.html', c)

def user_profile_create(sender, **kwargs):
    if kwargs['created']:
        profile = UserProfile(user=kwargs['instance']);
        profile.save();

post_save.connect(user_profile_create, sender=User)

# This needs to be reworked, maybe with user profiles
@login_required
def redirect_to_user(request, *args, **kwargs):
    redirect_to = '/users/%d' % (request.user.pk)
    return HttpResponseRedirect(redirect_to)

@login_required
def idea_create(request, *args, **kwargs):
    if request.method == 'POST':
        tags = request.POST["tags"]
        idea_POST = request.POST.copy()
        del(idea_POST["tags"])

        idea = Idea(owner=request.user.get_profile())
        idea_form = IdeaForm(idea_POST, instance=idea)
        if idea_form.is_valid():
            idea_form.save()
            idea.add_tags(tags)
            redirect_to = idea.get_absolute_url()
            return HttpResponseRedirect(redirect_to)
    else:
        idea_form = IdeaForm()

    kwargs.update(csrf(request))
    c = RequestContext(request, dict(form=idea_form, **kwargs))
    return render_to_response('main/idea_form.html', c)

@login_required
def idea_join(request, object_id, *args, **kwargs):
    idea = get_object_or_404(Idea, pk=object_id)
    try:
        idea.members.get(user=request.user.pk)
        return HttpResponse("You're already a member")
    except ObjectDoesNotExist:
        idea.add_member(request.user)
        redirect_to = idea.get_absolute_url()
        return HttpResponseRedirect(redirect_to)

@login_required
def idea_leave(request, object_id, *args, **kwargs):
    idea = get_object_or_404(Idea, pk=object_id)
    try:
        idea.members.get(user=request.user.pk)
        idea.remove_member(request.user)
        redirect_to = idea.get_absolute_url()
        return HttpResponseRedirect(redirect_to)
    except ObjectDoesNotExist:
        return HttpResponse("You aren't a member of this project")

def tag_suggest(request, **kwargs):
    json = serializers.get_serializer("json")()
    response = HttpResponse(mimetype="text/json")
    search = request.GET['s']
    json.serialize(Tag.objects.filter(name__istartswith=search),
                    fields=("name"), stream=response)
    return response
