from django.shortcuts import render_to_response,  redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from box_app import views as box
from dropbox_app import views as dropbox
from google_app.views import download_from_google, upload_to_google
from google_app.views import google_home, retrieve_all_files, refresh_google_token

from main_app.models import *
from main_app.settings import UPLOAD_FOLDER
from main_app.utils import *

import json
import os.path

def homepage( request ):
    """
    Index Page for user ( when he is not logged in )
    """
    if "email" in request.session:
        return redirect( '/home' )
    return render_to_response( 'index.html' )

def home( request ):
    """
    Logged in user landing page
    """
    user_email request.session["email"];
    box_data = box.dir_info( user_email,  '/' )
    dropbox_data = dropbox.dir_info( user_email,  '/' )
    google_data = retrieve_all_files( request.session["email"] )
    pending_share_dump = pendingShares( request )

    user_data = {
        "name" : user_name, 
        "email" : user_email
    }
    drive_stack = {
        "box_data" : json.dumps( box_data ), 
        "dropbox_data" : json.dumps( dropbox_data ), 
        "google_data": json.dumps( google_data )
    }
    sharing_info = {
        "pending_shares" : json.dumps( pending_share_dump ), 
    }
    params = dict( user_data.items( ) + drive_stack.items( ) + sharing_info.items( ) )

    return render_to_response( 'home.html',  params )

def home_saket( request ):
    data = refresh_google_token( request.session["email"] )
    return HttpResponse( data )

@csrf_exempt
def upload( request ):
    for name,  f in request.FILES.items( ):
        g = open( os.path.join( UPLOAD_FOLDER,  hash_email( email ) + f.name ),  'w' )
        g.write( f.read( ) )
        g.close( )
        box.upload_from_server( request.session["email"],  f.name,  "/" )
        return HttpResponse( name + f.name )

def cross_share_request( request ):
    from_email = request.session["email"]
    from_cloud = request.GET["from_cloud"]
    file_id = request.GET["fileid"]
    to_email = request.GET["to_email"]
    file_name = request.GET["file_name"]
    s = SharingInfo( shared_by = from_email, shared_with = to_email, shared_from_drive = from_cloud,  file_path_or_id = file_id, file_name = file_name )
    s.save( )
    return HttpResponse( "Share request sent" )

def cross_share_manifest( request ):
    to_email = request.session["email"]
    from_cloud = request.GET["shared_from_drive"]
    file_id = request.GET["file_path_or_id"]
    from_email = request.GET["shared_by"]

    to_cloud = Accounts.objects.filter( email = to_email ).values( "account_type" )[0]["account_type"]
    file_name = SharingInfo.objects.filter( shared_with = to_email ).filter( file_path_or_id = file_id ).values( "file_name" )[0]["file_name"]

    if from_cloud == "google":
        download_from_google( from_email,  file_id )
    elif from_cloud == "dropbox":
        dropboxdownload_server( from_email,  file_id )
    elif from_cloud == "box":
        box.download_to_server( from_email, file_id, file_name )

    if to_cloud == "google":
        uploadtogoogle( to_email,  file_id,  title,  mimetype,  desciption )
    elif to_cloud == "dropbox":
        dropbox.upload_from_server( to_email,  file_name,  "/" )
    elif to_cloud == "box":
        box.upload_from_server( to_email,  file_name,  "/" )

    return HttpResponse( "File Shared \m/" )

def pending_shares( request ):
    to_email = request.session["email"]
    shares = SharingInfo.objects.filter( shared_with = to_email ).values( )
    shares1 = []
    for i in shares:
        shares1.append( i )
    if len( shares1 ) == 0:
        shares1 = {}
    return shares1
