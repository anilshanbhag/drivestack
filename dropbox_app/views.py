# Create your views here.
from DropBoxClient import DropBoxClient
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect

def dropboxinterface(request,type):
    if type == "register":
        client = DropBoxClient()
        return redirect(client.register())

    if type == "oauthcallback":
        return HttpResponse(client.store_access_token)
        
        

