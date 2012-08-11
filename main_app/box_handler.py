import boxdotnet as box
from apikeys import *
from django.shortcuts import redirect

def box_account_handler(request):
    boxClient = box.BoxDotNet()
    redirect( boxClient.auth_url( BOX_API_KEY ) )
