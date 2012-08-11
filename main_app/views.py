from django.shortcuts import render_to_response
from django.http import HttpResponse
from box_handler import box_account_handler

def homepage(request):
    return render_to_response('index.html')

def addaccount(request, type):
    if type == "box":
        box_account_handler(request)
    return HttpResponse(type)
