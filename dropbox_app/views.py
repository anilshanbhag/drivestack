# Create your views here.
#from DropBoxClient import DropBoxClient
from django.shortcuts import render_to_response
from django.http import HttpResponse

def dropboxinterface(request):
    #if type == "register":
    return HttpResponse("hello u")


        #return DropBoxClient.register(request)

        
        
