# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Idea, User

def index(request):
    return render_to_response("main.html",
                              { "h1" : "Index"})
