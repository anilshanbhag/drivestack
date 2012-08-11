# Create your views here.
from dropbox import client, rest, session 
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

def dropboxinterface(request,type):
    if type == "register":
       
        sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        # Make the user sign in and authorize this token
        request.session["sess"]=sess
        return redirect( url+'&oauth_callback=http%3A%2F%2Fwncc.webfactional.com%2Fdropbox%2Foauthcallback')

    if type == "oauthcallback":
        #request_token = request.GET["request_token"]
        
        uid = request.GET["uid"]
        oauth_token=request.GET["oauth_token"]
        
        sess=request.session["sess"]
        #return HttpResponse(request_token)
        access_token = sess.obtain_access_token()
        access_headers=sess.build_access_headers('POST','https://api-content.dropbox.com/1/')
        json_access_header = json.dumps( access_headers )
        connected_client = client.DropboxClient(sess)
        info= connected_client.account_info()
        p = Accounts( email = info['email'], account_type = 'dropbox', account_data =json_access_header )
        p.save()
        return HttpResponse(connected_client.account_info().items())
        #sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        #access_token = sess.obtain_access_token(request_token)
        #self.client = client.DropboxClient(self.sess)

        
        

