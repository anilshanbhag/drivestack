from django.shortcuts import render_to_response
from django.http import HttpResponse
import boxdotnet as box
from apikeys import *
from django.shortcuts import redirect

def box_addaccount(request):
    boxClient = box.BoxDotNet()
    return redirect( boxClient.auth_url( BOX_API_KEY ) )

def box_oauthcallback(request):
    return HttpResponse("hello u")
