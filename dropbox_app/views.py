# Create your views here.
from DropBoxClient import DropBoxClient
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect

def dropboxinterface(request,type):
    if type == "register":
        client = DropBoxClient()
        return redirect(client.register())

    if type == "oauthcallback":
        client 
        access_token = sess.obtain_access_token(request_token)
        self.client = client.DropboxClient(sess)
        

