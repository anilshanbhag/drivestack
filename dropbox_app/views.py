# Create your views here.
from DropBoxClient import DropBoxClient
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect

def dropboxinterface(request,type):
    if type == "register":
        x = DropBoxClient()
        return redirect(x.register())

