import os
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import OAuth2Credentials
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import errors
from apiclient.discovery import build

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
static_folder=os.path.join(PROJECT_ROOT, 'static')

CLIENTSECRETS_LOCATION = os.path.join(static_folder,'CLIENT_SECRETS.JSON')
REDIRECT_URI = 'http://wncc.webfactional.com/google/oauthcallback'
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile',]
def google_addaccount(request):
    flow = OAuth2WebServerFlow(client_id='640541804881-qn8sn3la5ag395ptr341mtebf9s49ru2.apps.googleusercontent.com',client_secret='NAU1FwwH_m8Hi50APEfonoQZ',scope=SCOPES,user_agent='buzz-cmdline-sample/1.0')
    callback = 'http://wncc.webfactional.com/google/oauthcallback'
    authorize_url = flow.step1_get_authorize_url(callback)
    return redirect(authorize_url)
	
def receive_oauthcode(request):
    code = request.GET.get('code')



