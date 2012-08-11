from django.conf.urls.defaults import patterns, include, url
from views import home
from DropboxClient import DropboxClient
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'drivestack.views.home', name='home'),
    # url(r'^drivestack/', include('drivestack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    ('^$', home),
    (r'^static/(?P<path>.*)', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    (r'^addaccount/dropbox$', 'DropboxClient.register'),)
)
