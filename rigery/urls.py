from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from rigery.views import start_page, test_page
from authentication.views import sign_in, sign_out
from nginx_manager.views import nginx_configuration_editor

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rigery.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', start_page),
    url(r'#$', start_page),

    url(r'^test/', test_page),

    #Servers
    url(r'^nginx/', nginx_configuration_editor),

    url(r'^accounts/login/$', sign_in),
    url(r'^accounts/logout/$', sign_out),
)
