from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from rigery.views import start_page
from authentication.views import sign_in, sign_out
from nginx_manager.views import nginx_configuration_interface

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rigery.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', start_page),

    #Servers
    url(r'^nginx/', nginx_configuration_interface),

    url(r'^accounts/login/$', sign_in),
    url(r'^accounts/logout/$', sign_out),
)
