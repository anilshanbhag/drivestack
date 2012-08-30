from django.conf.urls.defaults import *
from main_app.views import homepage, home, upload, home_saket, crosssharerequest, crosssharemanifest
from dropbox_app.views import dropboxinterface
from box_app.views import box_addaccount, box_oauthcallback, box_download
from google_app.views import google_addaccount, google_oauthcallback, refresh_google_token
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', homepage),
    (r'^home$', home),

    (r'^homes$', home_saket),
    (r'^share$', crosssharerequest),
    (r'^shareaccept$', crosssharemanifest),
    (r'^upload$', upload),
    (r'^dropbox/([a-z]*)$', dropboxinterface),

    (r'^box/', include('box_app.urls')),
    (r'^google/', include('google_app.urls')),
    (r'^dropbox/', include('dropbox_app.urls')),
)
