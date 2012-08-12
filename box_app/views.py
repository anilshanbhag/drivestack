from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse

from apikeys import *
import json

import boxapi as box
from boxdotnet import BoxDotNet
from main_app.models import Accounts

def box_addaccount(request):
    boxClient = box.Session( BOX_API_KEY )
    boxClient.apply_new_authtoken()
    return redirect( boxClient.auth_url )
    # box_uploadfile("anilashanbhag@gmail.com")
    # return HttpResponse("done")

def box_oauthcallback(request):
    pars = { 'ticket' : request.GET["ticket"], 'auth_token' : request.GET["auth_token"] }
    pars_string = json.dumps( pars )
    boxClient = box.Session( BOX_API_KEY, auth_token = pars['auth_token'] )
    res = boxClient.get_account_info()
    email = res['response']['user']['email']['value']
    request.session["email"] = email
    p = Accounts( email = email, account_type = 'box', account_data = json.dumps(pars) )
    p.save()

    return redirect( '/home' ) 

def folder_details( email, path='/' ):
    if email == "":
        return "{}"
    accounts = Accounts.objects.filter(email = email, account_type = 'box')

    if len( accounts ) < 1:
        return "{}"

    account_data = json.loads( accounts[0].account_data )
    boxClient = box.Session( BOX_API_KEY, auth_token = account_data['auth_token'] )

    return boxClient.action("/folders/0")

def box_uploadfile( email,fileid,filename):
    box = BoxDotNet()

    accounts = Accounts.objects.filter(email = email, account_type = 'box')
    account_data = json.loads( accounts[0].account_data )
    data=open(os.path.join(UPLOAD_FOLDER,fileid),'r')
    box.upload(filename, data , api_key = BOX_API_KEY, auth_token = account_data['auth_token'], folder_id = "0")

def box_download( request, id ):
    email = request.session["email"]
    accounts = Accounts.objects.filter(email = email, account_type = 'box')
    account_data = json.loads( accounts[0].account_data )
    return redirect("https://www.box.net/api/1.0/download/%s/%s" % (account_data['auth_token'], id))

def box_download_helper( email, id ):
    accounts = Accounts.objects.filter(email = email, account_type = 'box')
    account_data = json.loads( accounts[0].account_data )
    return redirect("https://www.box.net/api/1.0/download/%s/%s" % (account_data['auth_token'], id))


