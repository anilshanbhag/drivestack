from django.shortcuts import render_to_response
from django.http import HttpResponse

def homepage(request):
    # request.session["name"] = "DSADSADSADSAD"
    return render_to_response('index.html')

def home(request):
    return render_to_response('home.html')

def upload(request):
    #
    #
    return render_to_response('home.html')
