from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse

from apikeys import *
import json
import os.path
import urllib2
from datetime import datetime

import boxapi as box
from boxdotnet import BoxDotNet
from main_app.models import Accounts
from main_app.settings import *

"""
Box Flow

OAuth Initiate => 


"""

def box_addaccount(request):
    boxClient = box.Session( BOX_API_KEY )
    boxClient.apply_new_authtoken( )
    return redirect( boxClient.auth_url )

def box_oauthcallback(request):
    pars = { 'ticket' : request.GET["ticket"], 'auth_token' : request.GET["auth_token"] }
    pars_string = json.dumps( pars )
    boxClient = box.Session( BOX_API_KEY, auth_token = pars['auth_token'] )
    
    res = boxClient.get_account_info()
    email = res['response']['user']['email']['value']
    request.session["email"] = email

    # Remove previous accounts
    p = Accounts.objects.filter(email= email, account_type = 'box')
    if len(p) >= 1:
        for acc in p: 
            acc.delete()

    # Add the account with new account details
    p = Accounts( email = email, account_type = 'box', account_data = json.dumps(pars))
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
    data=open(os.path.join(UPLOAD_FOLDER,fileid),'r').read()
    box.upload(filename, data , api_key = BOX_API_KEY, auth_token = account_data['auth_token'], folder_id = "0")

def box_download( request, id ):
    email = request.session["email"]
    accounts = Accounts.objects.filter(email = email, account_type = 'box')
    account_data = json.loads( accounts[0].account_data )
    f= urllib2.urlopen("https://www.box.net/api/1.0/download/%s/%s" % (account_data['auth_token'], id)).read()
    g = open(os.path.join(UPLOAD_FOLDER, id), 'wb')
    g.write(f)
    g.close()

def box_download_helper( email, id, name ):
    accounts = Accounts.objects.filter(email = email, account_type = 'box')
    account_data = json.loads( accounts[0].account_data )
    f= urllib2.urlopen("https://www.box.net/api/1.0/download/%s/%s" % (account_data['auth_token'], id)).read()
    g = open(os.path.join(UPLOAD_FOLDER, name), 'wb')
    g.write(f)
    g.close()
