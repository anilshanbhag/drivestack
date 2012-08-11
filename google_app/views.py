from django.shortcuts import render_to_response
from django.http import HttpResponse
import boxdotnet as box
from apikeys import *
from django.shortcuts import redirect
CLIENTSECRETS_LOCATION = os.path.join(static_folder,'CLIENT_SECRETS.JSON')
REDIRECT_URI = 'http://wncc.webfactional.com/google/oauthcallback'

def google_addaccount(request):
	low = OAuth2WebServerFlow(
              # Visit https://code.google.com/apis/console to
              # generate your client_id, client_secret and to
              # register your redirect_uri.
              client_id='640541804881-qn8sn3la5ag395ptr341mtebf9s49ru2.apps.googleusercontent.com',
              client_secret='NAU1FwwH_m8Hi50APEfonoQZ',
              scope=SCOPES,
              user_agent='buzz-cmdline-sample/1.0')
    callback = 'http://wncc.webfactional.com/google/oauthcallback'
    authorize_url = flow.step1_get_authorize_url(callback)
    return redirect(authorize_url)
	



