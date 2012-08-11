from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
import boxdotnet as box
from apikeys import *

def box_addaccount(request):
    boxClient = box.BoxDotNet()
    return redirect( boxClient.auth_url( BOX_API_KEY ) )

def box_oauthcallback(request):
    request.GET["ticket"]
    request.GET["auth_token"]
    return HttpResponse("hello u")
