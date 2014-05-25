from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from rigery.views import start_page, test_nginx
from authentication.views import sign_in, sign_out

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rigery.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', start_page),

    #Servers
    url(r'^nginx/', test_nginx),

    url(r'^accounts/login/$', sign_in),
    url(r'^accounts/logout/$', sign_out),
)
