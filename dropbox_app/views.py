# Create your views here.
from DropBoxClient import DropBoxClient
from django.shortcuts import render_to_response
from django.http import HttpResponse

def dropboxinterface(request,type):
    if type == "register":
        return DropBoxClient.register(request)
        
        #return HttpResponse(type)



        
        
