from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from box_app.views import folder_details
from dropbox_app.views import dropboxfiles
from main_app.models import *
from google_app.views import download_from_google,upload_to_google
from dropbox_app.views import dropboxdownload_server,dropboxupload_server
from box_app.views import box_download_helper,box_uploadfile
from google_app.views import google_home,retrieve_all_files
import json

def homepage(request):
    # request.session["name"] = "DSADSADSADSAD"
    return render_to_response('index.html')

def home(request):
    # data = google_home(request.session["email"])
    # return HttpResponse(data)
    dump = folder_details( request.session["email"], '/' )
    dropboxdump =  dropboxfiles(request)
    googledata = retrieve_all_files(request.session["email"])
    pendingShareDump = pendingShares(request)
    params = {
        "boxData" : json.dumps(dump),
        "dropboxData" : json.dumps(dropboxdump),
        "pendingShares" : json.dumps(pendingShareDump),
        "googleData": json.dumps(googledata),
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

def crosssharerequest(request):
    fromemail = request.session["email"]
    fromcloud=request.GET["fromcloud"]
    fileid=request.GET["fileid"]
    toemail=request.GET["toemail"]
    s = SharingInfo(shared_by=fromemail,shared_with=toemail,shared_from_drive = fromcloud, file_path_or_id = fileid)
    s.save()
    return HttpResponse("Share request sent")

def crosssharemanifest(request):
    fromemail = request.session["email"]
    tocloud=Accounts.objects.filter(email=toemail).values["account_type"][0]["account_type"]
    if fromcloud == "google":
        download_from_google(fromemail,fileid)
    if fromcloud == "dropbox":
        dropboxdownload_server(fromemail,fileid)
    if fromcloud == "box":
        box_download_helper(fromemail,fileid)

    #  if tocloud == "google":
    #      uploadtogoogle(toemail,content,title,mimetype,desciption)

    if tocloud == "dropbox":
        dropboxupload_server(toemail,fileid)
    if tocloud == "box":
        box_uploadfile(toemail,fileid)
def pendingShares(request):
    toemail=request.session["email"]
    return SharingInfo.objects.filter(shared_with=toemail).values()
