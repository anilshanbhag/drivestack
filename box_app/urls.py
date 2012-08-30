from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^box/login', views.box_addaccount),
    (r'^box/addaccount', views.box_addaccount),
    (r'^box/oauthcallback', views.box_oauthcallback),
    (r'^box/download/(\d+)', views.box_download),
)
