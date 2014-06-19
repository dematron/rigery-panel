from django.shortcuts import render

from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import *
from django.views.decorators.csrf import csrf_protect
from scripts.config_rw.nginx_config_reader import NginxConfigReader
import constant

#load data from nginx.conf
def load_config():
    reader = NginxConfigReader()
    try:
        result = reader.read(constant.DEFAULT_NGINX_LOCATION)
    except IOError:
        return [-1, None]
    else:
        block_main = result["main"]
        return [0, block_main]

@login_required
@csrf_protect
def nginx_configuration_interface(request):
    if request.is_ajax():
        if request.method == 'GET':
            print "GET"
            print request
        elif request.method == 'POST':
            print "POST"
            print request.POST
        return render_to_response("nginx_manager/nginx_configuration.html", context_instance=RequestContext(request))
    else:
        response = load_config()
        if response[0] == 0:
            result = response[1]
            return render_to_response(
                "nginx_manager/nginx_configuration.html",
                result,
                context_instance=RequestContext(request),
            )
