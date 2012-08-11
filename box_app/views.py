from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
import boxdotnet as box
from apikeys import *
import json

def box_addaccount(request):
    boxClient = box.BoxDotNet()
    return redirect( boxClient.auth_url( BOX_API_KEY ) )

def box_oauthcallback(request):
    pars = { 'ticket' : request.GET["ticket"], 'auth_token' : request.GET["auth_token"] }
    pars_string = json.dumps( pars )
    boxClient = box.BoxDotNet()
    res = boxClient.get_account_info( auth_token = request.GET["auth_token"] )
    return HttpResponse(json.dumps(res))
