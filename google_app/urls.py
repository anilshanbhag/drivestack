from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^google/addaccount', views.google_addaccount),
    (r'^google/oauthcallback', views.google_oauthcallback),
    (r'^google/refreshtoken', views.refresh_google_token),
)
