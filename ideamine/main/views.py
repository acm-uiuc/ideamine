# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.template import RequestContext
from main.forms import *
from main.models import *

def index(request):
    c = RequestContext(request, { 'h1' : 'Index' })
    return render_to_response("main.html", c)

def members(request, object_id=None):
    if not object_id:
        raise Http404
    return render_to_response("users.html",
        { 'object_list' : Idea.objects.get(id=object_id).members.all(),
          'h1' : 'members' })

@login_required
def idea_create(request, *args, **kwargs):
    if request.method == 'POST':
        idea = Idea(owner=request.user)
        idea_form = IdeaForm(request.POST, instance=idea)
        if idea_form.is_valid:
            idea_form.save()
            redirect_to = idea.get_absolute_url()
            return HttpResonseRedirect(redirect_to)
    else:
        idea_form = IdeaForm()

    kwargs.update(csrf(request))
    c = RequestContext(request, dict(form=idea_form, **kwargs))
    return render_to_response('main/idea_form.html', c)

@login_required
def idea_join(request, *args, **kwargs):
    idea = get_object_or_404(Idea, pk=object_id)
    return HttpResponse("The goggles! They do nothing!")
