# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Idea

def index(request):
    return render_to_response("main.html",{ "h1" : "Index"})

def users(request, user_id=None):
    return render_to_response("users.html",{ "h1" : "Users"})

def ideas(request, request_id=None):
    return render_to_response("ideas.html",{ "h1" : "Ideas", "ideas" : Idea.objects.all() })
