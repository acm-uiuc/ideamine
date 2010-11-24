# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import list_detail
from models import Idea, User

def index(request):
    return render_to_response("main.html",
                              { "h1" : "Index"})

def members(request, template_name=None, object_id=None):
    return list_detail.object_list(request, queryset = Idea.objects.get(id=object_id).members.all(), template_name = template_name)
