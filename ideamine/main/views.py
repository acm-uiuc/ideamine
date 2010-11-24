# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.views.generic import list_detail
from models import Idea, User

def index(request):
    return render_to_response("main.html",
                              { "h1" : "Index"})

def members(request, object_id=None):
    if not object_id:
        raise Http404
    return render_to_response("users.html",
        { 'object_list' : Idea.objects.get(id=object_id).members.all(),
          'h1' : 'members' })
