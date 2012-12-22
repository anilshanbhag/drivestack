from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^add_account', views.add_account),
    (r'^login', views.add_account),
    (r'^oauth_callback', views.oauth_callback),
)
