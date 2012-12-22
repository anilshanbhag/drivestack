from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^login', views.add_account),
    (r'^add_account', views.add_account),
    (r'^oauth_callback', views.oauth_callback),
    (r'^download/(\d+)', views.download),
)
