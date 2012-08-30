from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^box/login', views.add_account),
    (r'^box/addaccount', views.add_account),
    (r'^box/oauthcallback', views.oauth_callback),
    (r'^box/download/(\d+)', views.download),
)
