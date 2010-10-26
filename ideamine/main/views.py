# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return render_to_response("main.html",{ "h1" : "Index"})

def users(request, user_id=None):
    response = "Users"
    if (user_id):
        response = "%s<br/>User id: %s" % (response, user_id)
    return HttpResponse(response)
