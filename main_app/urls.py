from django.conf.urls import patterns, include, url
from main_app.views import homepage, home, upload
from dropbox_app.views import dropboxinterface
from box_app.views import box_addaccount, box_oauthcallback
from google_app.views import google_addaccount, google_oauthcallback
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
# Examples:
# url(r'^$', 'myproject.views.home', name='home'),
# url(r'^myproject/', include('myproject.foo.urls')),

# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# Uncomment the next line to enable the admin:
# url(r'^admin/', include(admin.site.urls)),
    (r'^$', homepage),
    (r'^home', home),
    (r'^upload$', upload),
    (r'^dropbox/([a-z]*)$', dropboxinterface),
    (r'^box/addaccount', box_addaccount),
    (r'^box/oauthcallback', box_oauthcallback),
    (r'^google/addaccount', google_addaccount),
    (r'^google/oauthcallback', google_oauthcallback),

)
