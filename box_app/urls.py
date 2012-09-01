from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^box/login', views.add_account),
    (r'^box/add_account', views.add_account),
    (r'^box/oauth_callback', views.oauth_callback),
    (r'^box/download/(\d+)', views.download),
)
