from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt    
import json

def homepage(request):
    # request.session["name"] = "DSADSADSADSAD"
    return render_to_response('index.html')

def home(request):
    return render_to_response('home.html')

@csrf_exempt
def upload(request):
    # request.FILES
    for name, file in request.FILES.items():
        return HttpResponse(file.name + file.read()) #render_to_response('home.html')
