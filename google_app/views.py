import os
import urllib
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
from main_app import settings
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
upload_path = settings.UPLOAD_FOLDER
static_folder=os.path.join(PROJECT_ROOT, 'static')

CLIENTSECRETS_LOCATION = os.path.join(static_folder,'CLIENT_SECRETS.JSON')
REDIRECT_URI = 'http://wncc.webfactional.com/google/oauthcallback'
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile',]
#def insert_file(service,title,description,mime_type
def upload_to_google(email,content,title="New Document from DriveStack",mimetype="text/plain",description="this has been uploaded by Drivestack"):
    
    all_data = GoogleData.objects.filter(email=email).values()[0]
    #return HttpResponse(str(all_data))
    credentials = OAuth2Credentials(str(all_data["access_token"]),str(all_data["client_id"]),str(all_data["client_secret"]),str(all_data["refresh_token"]),str(all_data["token_expiry"]),str(all_data["token_uri"]),str(all_data["user_agent"]))
    service = builds_service(credentials)
    service_handler = ServiceHandler()
    file_id = service_handler.post(service,mime_type,content,title,description)
    #file_content  =service_handler.service,file_id)
    return HttpResponse("File ID: "+file_id)

def download_from_google(email,file_id):
    all_data = GoogleData.objects.filter(email=email).values()[0]
    #return HttpResponse(str(all_data))
    credentials = OAuth2Credentials(str(all_data["access_token"]),str(all_data["client_id"]),str(all_data["client_secret"]),str(all_data["refresh_token"]),str(all_data["token_expiry"]),str(all_data["token_uri"]),str(all_data["user_agent"]))
    service = builds_service(credentials)
    service_handler = ServiceHandler()
    response = service_handler.get(service,file_id)
    content = response['content']
    title = response['title']
    f=open(os.path.join(upload_path,file_id),'w')
    f.write(content)
    f.close()
    return title
    
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
    google_data = GoogleData(uid=str(uid),email=str(email),access_token=access_token,client_id=client_id,client_secret=client_secret,refresh_token=refresh_token,token_expiry=token_expiry,token_uri=token_uri,user_agent=user_agent,id_token=id_token)
    google_data.save()
    account_data = Accounts(email=email,name='',account_type='google',account_data=all_data)
    account_data.save()

    
    
def builds_service(credentials):
    http = httplib2.Http()
    http_auth = credentials.authorize(http)
    return build('drive', 'v2', http=http_auth)

def retrieve_all_files(email):
    result = []
    try:
        all_data = GoogleData.objects.filter(email=email).values()[0]
    except:
        return "{}"
    #return HttpResponse(str(all_data))
    credentials = OAuth2Credentials(str(all_data["access_token"]),str(all_data["client_id"]),str(all_data["client_secret"]),str(all_data["refresh_token"]),str(all_data["token_expiry"]),str(all_data["token_uri"]),str(all_data["user_agent"]))
    service = builds_service(credentials)
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
    test = ""
    json_return = []
    i=0
    for values in result:
        try:
            test = test + "----------------" + str(values)
            mimeType = str(values.get('mimeType'))
            if mimeType== "application/vnd.google-apps.folder":
                is_dir = "True"
            else:
                is_dir="False"
            json_return.append({"id":str(values.get("id")),"title":str(values.get('title')),"is_dir":is_dir,"modified":str(values.get("modifiedDate"))})
        except:
            test = test

        #json_return.append(str(values.get("title")))
        i+=1

    return str(json_return)

def google_addaccount(request):
    flow = OAuth2WebServerFlow(client_id='640541804881-qn8sn3la5ag395ptr341mtebf9s49ru2.apps.googleusercontent.com',client_secret='NAU1FwwH_m8Hi50APEfonoQZ',scope=SCOPES,user_agent='buzz-cmdline-sample/1.0')
    callback = 'http://wncc.webfactional.com/google/oauthcallback'
    authorize_url = flow.step1_get_authorize_url(callback)
    return redirect(authorize_url)


#def upload_google_file()    
def refresh_google_token(email):
    #email = request.session["email"]
    refresh_token = GoogleData.objects.filter(email=email).values('refresh_token')[0]["refresh_token"]
    query = urllib.urlencode({'token':refresh_token})
    http = httplib2.Http()
    access_token = http.request(('https://accounts.google.com/o/oauth2/revoke?' + query), 'GET')
    return str(access_token)

def google_home(email):
    #refresh_google_token(email)
    all_data = GoogleData.objects.filter(email=email).values()[0]
    #return HttpResponse(str(all_data))
    credentials = OAuth2Credentials(str(all_data["access_token"]),str(all_data["client_id"]),str(all_data["client_secret"]),str(all_data["refresh_token"]),str(all_data["token_expiry"]),str(all_data["token_uri"]),str(all_data["user_agent"]))
    #try:
    service = builds_service(credentials)
    #except:
        #refresh_google_token(all_data["email"])
        #service = builds_service(credentials)
    return str(retrieve_all_files(service))

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
    request.session["email"] = email
    if not is_returning_user(email):
        add_to_db(uid,email,access_token,client_id,client_secret,refresh_token,token_expiry,token_uri,user_agent,id_token,email)
        #return HttpResponse("Added to DB")
        return redirect("/google/addaccount")
    else:
        return redirect("/home")
        """try:
            credentials = OAuth2Credentials(access_token,client_id,client_secret,refresh_token,token_expiry,token_uri,user_agent)
            service = builds_service(credentials)
            #post_data = ServiceHandler()
            
            #id = post_data.post(service)
            #file_content  = post_data.get(service,id)
            return HttpResponse("File Contents: "+str(retrieve_all_files(service)))
        except:
            #return render_to_response("templates/index.html")
            return HttpResponse("DSADADA")"""

