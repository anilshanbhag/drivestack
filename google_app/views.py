import os
import json
import httplib2
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import OAuth2Credentials
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import errors
from apiclient.discovery import build
from main_app.models import Accounts
from google_app.models import GoogleData
from google_app.drive_uploader import ServiceHandler
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
static_folder=os.path.join(PROJECT_ROOT, 'static')

CLIENTSECRETS_LOCATION = os.path.join(static_folder,'CLIENT_SECRETS.JSON')
REDIRECT_URI = 'http://wncc.webfactional.com/google/oauthcallback'
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile',]
#def insert_file(service,title,description,mime_type
def is_returning_user(email):
    try:
        user = Accounts.objects.get(email=email,account_type="google")
        return True
    except:
        return False
    
    
    
def get_user_info(credentials):
    user_info_service = build(serviceName='oauth2', version='v2',http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
    except :
        return  "error 2"
    if user_info and user_info.get('id'):
        return user_info
    else:
        return "error getting useringfo"

def exchange_code(authorization_code):
    try:
        flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(SCOPES))
    except:
        return "erro reading file"
    try:
        flow.redirect_uri = REDIRECT_URI
    except:
        return "errir redirct ut"
    try:
        credentials = flow.step2_exchange(authorization_code)
        return credentials
    except FlowExchangeError:
        #logging.error('An error occurred: %s', error)
        return "ERROR"

def add_to_db(uid,email,access_token,client_id,client_secret,refresh_token,token_expiry,token_uri,user_agent,id_token,all_data):
    google_data = GoogleData('',str(uid),str(email),access_token,client_id,client_secret,refresh_token,token_expiry,token_uri,user_agent,id_token)
    google_data.save()
    account_data = Accounts('',email,'','google',all_data)
    account_data.save()

    
    
def builds_service(credentials):
    http = httplib2.Http()
    http_auth = credentials.authorize(http)
    return build('drive', 'v2', http=http_auth)
def retrieve_all_files(service):
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()
            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                result.append("ERROR")
                break
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            result.append(error)
            break
    return HttpResponse(result)

def google_addaccount(request):
    flow = OAuth2WebServerFlow(client_id='640541804881-qn8sn3la5ag395ptr341mtebf9s49ru2.apps.googleusercontent.com',client_secret='NAU1FwwH_m8Hi50APEfonoQZ',scope=SCOPES,user_agent='buzz-cmdline-sample/1.0')
    callback = 'http://wncc.webfactional.com/google/oauthcallback'
    authorize_url = flow.step1_get_authorize_url(callback)
    return redirect(authorize_url)

#def upload_google_file()    
def google_oauthcallback(request):
    code = request.GET.get('code')
    credentials =  exchange_code(code)
    credentials_json = json.loads(credentials.to_json())
    user_info = get_user_info(credentials)
    access_token = str(credentials_json["access_token"])
    client_id = str(credentials_json["client_id"])
    client_secret = str(credentials_json["client_secret"])
    refresh_token = str(credentials_json["refresh_token"])
    token_expiry = str(credentials_json["token_expiry"])
    token_uri = str(credentials_json["token_uri"])
    user_agent = str(credentials_json["user_agent"])
    id_token = str(credentials_json["id_token"])
    uid = str(user_info.get('id'))
    email = str(credentials_json["id_token"]["email"])
    if not is_returning_user(email):
        add_to_db(uid,email,access_token,client_id,client_secret,refresh_token,token_expiry,token_uri,user_agent,id_token,email)
        return HttpResponse("Added to DB")
    else:
        try:
            credentials = OAuth2Credentials(access_token,client_id,client_secret,refresh_token,token_expiry,token_uri,user_agent)
            service = builds_service(credentials)
            post_data = ServiceHandler()
            id = post_data.post(service)
            return HttpResponse("TEST"+id)
        except:
            #return render_to_response("templates/index.html")
            return HttpResponse("DSADADA")
