__author__ = 'kutepoval'

from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import *
import scripts.monitoring.get_host_info as host_info
from django.views.decorators.csrf import csrf_protect

@login_required
@csrf_protect
def test_nginx(request):
    if request.is_ajax():
        if request.method == 'GET':
            print "GET"
            print request
        elif request.method == 'POST':
            print "POST"
            print request.POST
    else:
        print "NONE"
        print request.GET
        print request.POST
    return render_to_response("servers/nginx_configuration.html", context_instance=RequestContext(request))

@login_required
def start_page(request):
    return render_to_response("index.html", host_info.get_host_info())
