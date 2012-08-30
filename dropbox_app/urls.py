from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^dropbox/([a-z]*)$', views.dropboxinterface),
)
