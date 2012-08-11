from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse

from apikeys import *
import json

import boxapi as box

def box_addaccount(request):
    boxClient = box.Session( BOX_API_KEY )
    boxClient.apply_new_authtoken()
    return redirect( boxClient.auth_url( BOX_API_KEY ) )

def box_oauthcallback(request):
    pars = { 'ticket' : request.GET["ticket"], 'auth_token' : request.GET["auth_token"] }
    pars_string = json.dumps( pars )
    boxClient = box.BoxDotNet()
    res = boxClient.get_account_info( auth_token = request.GET["auth_token"] )
    return HttpResponse(json.dumps(res))
