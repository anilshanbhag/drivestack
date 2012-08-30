from django.conf.urls.defaults import *
import main_app.views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    (r'^$', main_app.views.homepage),
    (r'^home$', main_app.views.home),
    (r'^share$', main_app.views.crosssharerequest),
    (r'^shareaccept$', main_app.views.crosssharemanifest),
    (r'^upload$', main_app.views.upload),
    (r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    (r'^box/', include('box_app.urls')),
    (r'^google/', include('google_app.urls')),
    (r'^dropbox/', include('dropbox_app.urls')),
)
