from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from box_app.views import folder_details
from main_app.models import *
from google_app.views import google_home
import json

def homepage(request):
    # request.session["name"] = "DSADSADSADSAD"
    return render_to_response('index.html')

def home(request):
    # data = google_home(request.session["email"])
    # return HttpResponse(data)
    dump = folder_details( request.session["email"], '/' )
    params = {
        "boxData" : json.dumps(dump)    
    }
    return render_to_response('home.html', params)

def home_saket(request):
    data = google_home(request.session["email"])
    return HttpResponse(data)
@csrf_exempt
def upload(request):
    # request.FILES
    for name, file in request.FILES.items():
        return HttpResponse(file.name + file.read()) #render_to_response('home.html')
'''

def crosssharerequest(request,fromcloud,toemail,fileid,filename):
    fromemail = request.session["email"]
    s = SharingInfo(shared_by=fromemail,shared_with=toemail,shared_from_drive = fromcloud, file_path_or_id = fileid,file_name=filename)
    s.save()

def crosssharemanifest(request,fromcloud,toemail,fileid)
    fromemail = request.session["email"]
    tocloud=Accounts.objects.filter(email=toemail).values["account_type"].[0]["account_type"]
    if fromcloud == "google":
        downloadfromgoogle(fromemail,fileid)
    if fromcloud == "dropbox":
        dropboxdownload_server(fromemail,fileid)
    if fromcloud == "box":
        box_download_helper(fromemail,fileid)

    if tocloud == "google":
        uploadtogoogle(toemail,content,title,mimetype,desciption)
    if tocloud == "dropbox":
        dropboxupload_server(toemail,fileid)
    if tocloud == "box":


        

    HttpResponse
    
    


def 
'''
