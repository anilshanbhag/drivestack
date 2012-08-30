from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from box_app.views import folder_details
from dropbox_app.views import dropboxfiles
from main_app.models import *
from google_app.views import download_from_google,upload_to_google
from dropbox_app.views import dropboxdownload_server,dropboxupload_server
from box_app.views import box_download_helper,box_uploadfile
from google_app.views import google_home,retrieve_all_files,refresh_google_token
import json
import os.path
from main_app.settings import UPLOAD_FOLDER
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
    data = refresh_google_token(request.session["email"])
    return HttpResponse(data)

@csrf_exempt
def upload(request):
# request.FILES
#    res = ""

    for name, f in request.FILES.items():
        g = open(os.path.join(UPLOAD_FOLDER,f.name), 'wb')
        g.write(f.read())
        g.close()
        # dropboxupload_server(request.session["email"], f.name)
        box_uploadfile(request.session["email"], f.name, f.name)
        return HttpResponse(name + f.name)
#    res += file



def crosssharerequest(request):
    fromemail = request.session["email"]
    fromcloud=request.GET["fromcloud"]
    fileid=request.GET["fileid"]
    toemail=request.GET["toemail"]
    filename=request.GET["filename"]
    s = SharingInfo(shared_by=fromemail,shared_with=toemail,shared_from_drive = fromcloud, file_path_or_id = fileid,file_name=filename)
    s.save()
    return HttpResponse("Share request sent")

def crosssharemanifest(request):
    toemail = request.session["email"]
    fromcloud=request.GET["shared_from_drive"]
    fileid=request.GET["file_path_or_id"]
    fromemail=request.GET["shared_by"]
    tocloud = Accounts.objects.filter(email=toemail).values("account_type")[0]["account_type"]
    filename = SharingInfo.objects.filter(shared_with=toemail).filter(file_path_or_id=fileid).values("file_name")[0]["file_name"]
    if fromcloud == "google":
        download_from_google(fromemail,fileid)
    if fromcloud == "dropbox":
        dropboxdownload_server(fromemail,fileid)
    if fromcloud == "box":
        box_download_helper(fromemail,fileid,filename)

    if tocloud == "google":
        uploadtogoogle(toemail,fileid,title,mimetype,desciption)

    if tocloud == "dropbox":
        dropboxupload_server(toemail,fileid)
    if tocloud == "box":
        box_uploadfile(toemail,fileid, filename)
    return HttpResponse("File Shared \m/")

def pendingShares(request):
    toemail=request.session["email"]
    shares = SharingInfo.objects.filter(shared_with=toemail).values()
    shares1 = []
    for i in shares:
        shares1.append(i)
    if len(shares1) == 0:
        shares1 = {}
    return shares1
