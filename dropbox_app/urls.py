from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^dropbox/add_account', views.add_account),
    (r'^dropbox/login', views.add_account),
    (r'^dropbox/oauth_callback', views.oauth_callback),
)
