# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Idea

def index(request):
    return render_to_response("main.html",
                              { "h1" : "Index"})

def user(request, user_id):
    return render_to_response("user.html",
                              { "user" : User.objects.filter(id=user_id) })

def idea(request, request_id):
    return render_to_response("idea.html",
                              { "idea" : Idea.objects.filter(id=request_id) })
