from dropbox import client, session
from config import *

import os.path
import json

from main_app.models import *
from django.http import HttpResponse
from django.shortcuts import redirect
from main_app.settings import UPLOAD_FOLDER
from main_app.utils import *

def get_session():
    """ Return a Dropbox Session """
    return session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

def add_account(request):
    """
    Add a dropbox account
    End point of /dropbox/login & /dropbox/add_account
    """
    sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
    request.session["sess"] = sess
    return redirect( url+'&oauth_callback=http%3A%2F%2Fwncc.webfactional.com%2Fdropbox%2Foauth_callback')

def oauth_callback(request):
    """
    OAuth Callback Endpoint
    If new account added - Add into database
    Else Do nothing
    """
    sess = request.session["sess"]
    access_token = sess.obtain_access_token()
    json_access_token = json.dumps((str(access_token.key),str(access_token.secret)))
    connected_client = client.DropboxClient(sess)
    info= connected_client.account_info()
    request.session["email"] = info["email"]
    if ( Accounts.objects.filter( email = info["email"], account_type="dropbox" ).values('account_data').count() == 0 ):
        p = Accounts( email = info['email'], account_type = 'dropbox', account_data = json_access_token )
        p.save()
    return redirect('/home')

def dir_info( email, path = "/"):
    """ Returns files of user given email id """
    if( Accounts.objects.filter(email = email).filter(account_type="dropbox").values('account_data').count() == 0 ):
        return ""
    connected_client = connect_client_email(email)
    home_content = connected_client.metadata(path)["contents"]
    less_home_content = []
    for inner in home_content:
        for key in ['bytes','icon','mime_type','rev','revision','root','thumb_exists','client_mtime']:
            if inner.has_key(key):
                del inner[key]
        less_home_content.append(inner)
    return less_home_content

def connect_client_email( email ):
    """  Returns a Dropbox Client for the given email id """
    access_token = json.loads(Accounts.objects.filter( email = email, account_type = "dropbox").values('account_data')[0]["account_data"])
    sess = get_session()
    sess.set_token(access_token[0], access_token[1])
    connected_client = client.DropboxClient(sess)
    return connected_client

def upload_from_server( email, fileid, path):
    """ Upload file to dropbox to given user account """
    connected_client = connect_client_email(email)
    file=open(os.path.join(UPLOAD_FOLDER,fileid),'r')
    connected_client.put_file(fileid,file)

def download_to_server( email, path ):
    """ Download file to given user account """
    out = open(os.path.join(UPLOAD_FOLDER,path),'w')
    connected_client = connect_client_email( email )
    data = connected_client.get_file(os.path.join('/',path)).read()
    out.write( data )

def copy( fromemail, path):
    access_token = json.loads(Accounts.objects.filter(email=fromemail).filter(account_type="dropbox").values('account_data')[0]["account_data"])
    sess = get_session()
    sess.set_token(access_token[0], access_token[1])
    from_client = client.DropboxClient(sess)
    from_cp_ref=from_client.createcopyref(path)
    to_client=connect_client(request)
    to_client.add_copy_ref(from_cp_ref,path)
    return dropbox_files(request)
