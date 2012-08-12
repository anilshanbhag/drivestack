# Create your views here.
import os.path
from dropbox import client, rest, session 
#from web_upload_app import Example
from main_app.models import *
APP_KEY = 'nqqr4e3g6fqiugf' 
APP_SECRET= 'ulw7g239slu521p' 
ACCESS_TYPE = 'dropbox' 
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect
from pprint import pprint
from main_app.models import Accounts
import json
from main_app.settings import UPLOAD_FOLDER
def get_session():
    return session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

def get_client(access_token):
    sess = get_session()
    sess.set_token(access_token.key, access_token.secret)
    return client.DropboxClient(sess)

def dropboxinterface(request,type):
    if (type == "addaccount"):
        sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        request.session["sess"]=sess
        return redirect( url+'&oauth_callback=http%3A%2F%2Fwncc.webfactional.com%2Fdropbox%2Foauthcallback')

    if (type == "oauthcallback"):
        sess=request.session["sess"]
        access_token = sess.obtain_access_token()
        json_access_token = json.dumps((str(access_token.key),str(access_token.secret)))
        connected_client = client.DropboxClient(sess)
        info= connected_client.account_info()
        if(Accounts.objects.filter(email=request.session["email"]).filter(account_type="dropbox").values('account_data').count() == 0):
            p = Accounts( email = info['email'], account_type = 'dropbox', account_data =json_access_token )
            p.save()
        request.session["email"]=info["email"]
        return redirect('/dropbox/existing')


    if type == "existing":
        connected_client=connect_client(request)
        #myfile=open(os.path.join(UPLOAD_FOLDER,'wsgi.py'),'r')
        #dropboxupload(request,'web_upload_app-test.py',myfile)
        #dropboxdownload(request,'proto.py')
        #myfile=open(os.path.join(UPLOAD_FOLDER,'wsgi.py'),'r')
        
        #TODO : empty root handling
        return redirect ('/home')

    if type == "refresh":
        return dropboxfiles(request)

        

def dropboxfiles(request):
    connected_client=connect_client(request)
    home_content = connected_client.metadata("/")["contents"]
    less_home_content = []
    for inner in home_content:
        for key in ['bytes','icon','mime_type','rev','revision','root','thumb_exists','client_mtime']:
            if inner.has_key(key):
                del inner[key]
        less_home_content.append(inner)
    return less_home_content

def connect_client(request):
    access_token = json.loads(Accounts.objects.filter(email=request.session["email"]).filter(account_type="dropbox").values('account_data')[0]["account_data"])
    sess = get_session()
    sess.set_token(access_token[0], access_token[1])
    connected_client = client.DropboxClient(sess)
    return connected_client

def connect_client_email(givenemail):
    access_token = json.loads(Accounts.objects.filter(email=givenemail).filter(account_type="dropbox").values('account_data')[0]["account_data"])
    sess = get_session()
    sess.set_token(access_token[0], access_token[1])
    connected_client = client.DropboxClient(sess)
    return connected_client

def dropboxupload(request,fileid):
    connected_client = connect_client(request)
    file=open(os.path.join(UPLOAD_FOLDER,fileid),'r')
    connected_client.put_file(fileid,file)
    
def dropboxupload_server(toemail,fileid):
    connected_client = connect_client_email(toemail)
    file=open(os.path.join(UPLOAD_FOLDER,fileid),'r')
    connected_client.put_file(fileid,file)

def dropboxdownload(request,path):
    out = open(os.path.join(UPLOAD_FOLDER,path),'w')
    connected_client = connect_client(request)
    file = connected_client.get_file(os.path.join('/',path)).read()
    out.write(file)
    
def dropboxdownload_server(fromemail,path):
    out = open(os.path.join(UPLOAD_FOLDER,path),'w')
    connected_client = connect_client_email(fromemail)
    file = connected_client.get_file(os.path.join('/',path)).read()
    out.write(file)

def dropboxcopy(fromemail,path):
    access_token = json.loads(Accounts.objects.filter(email=fromemail).filter(account_type="dropbox").values('account_data')[0]["account_data"])
    sess = get_session()
    sess.set_token(access_token[0], access_token[1])
    from_client = client.DropboxClient(sess)
    from_cp_ref=from_client.createcopyref(path)
    to_client=connect_client(request)
    to_client.add_copy_ref(from_cp_ref,path)
    return dropboxfiles(request)
    
    
    
    

    
