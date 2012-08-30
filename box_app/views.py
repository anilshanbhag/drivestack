from django.shortcuts import redirect

from apikeys import *
import json
import os.path
import urllib2

import boxapi as box
from boxdotnet import BoxDotNet
from main_app.models import Accounts
from main_app.settings import *
from main_app.utils import *

"""
STATUS:

add_account - done
oauth_callback - done
download -
download_to_server - done
upload_from_server - done (path ignored)
dir_info - done

"""


def add_account(request):
    boxClient = box.Session( BOX_API_KEY )
    boxClient.apply_new_authtoken( )
    return redirect( boxClient.auth_url )

def oauth_callback(request):
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

def dir_info( email, path='/' ):
    if email == "":
        return "{}"
    accounts = Accounts.objects.filter(email = email, account_type = 'box')

    if len( accounts ) < 1:
        return "{}"

    account_data = json.loads( accounts[0].account_data )
    boxClient = box.Session( BOX_API_KEY, auth_token = account_data['auth_token'] )

    return boxClient.action("/folders/0")

def upload_from_server( email, filename, path = '/' ):
    box = BoxDotNet()
    accounts = Accounts.objects.filter(email = email, account_type = 'box')
    account_data = json.loads( accounts[0].account_data )
    datapath = os.path.join(UPLOAD_FOLDER,hash_email(email) + filename)
    box.upload(filename, datapath , api_key = BOX_API_KEY, auth_token = account_data['auth_token'], folder_id = "0")

def download( request ):
    email = request.session["email"]
    accounts = Accounts.objects.filter(email = email, account_type = 'box')
    account_data = json.loads( accounts[0].account_data )
    f= urllib2.urlopen("https://www.box.net/api/1.0/download/%s/%s" % (account_data['auth_token'], id)).read()
    g = open(os.path.join(UPLOAD_FOLDER, id), 'wb')
    g.write(f)
    g.close()

def download_to_server( email, path ):
    accounts = Accounts.objects.filter(email = email, account_type = 'box')
    account_data = json.loads( accounts[0].account_data )
    f= urllib2.urlopen("https://www.box.net/api/1.0/download/%s/%s" % (account_data['auth_token'], path)).read()
    g = open(os.path.join(UPLOAD_FOLDER, hash_email(email) + file_name), 'w')
    g.write(f)
    g.close()
