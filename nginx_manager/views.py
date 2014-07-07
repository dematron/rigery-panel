from django.shortcuts import render

from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import *
from django.views.decorators.csrf import csrf_protect
from scripts.config_rw.nginx_config_parser import NginxConfigParser, NginxConfigRW
import constant

#load data from nginx.conf
def load_config():
    reader = NginxConfigParser()
    try:
        result = reader.read(constant.DEFAULT_NGINX_LOCATION)
    except IOError:
        return [-1, None]
    else:
        block_main = result["main"]
        block_main["nginx_conf_location"] = constant.DEFAULT_NGINX_LOCATION
        return [0, block_main]

@login_required
@csrf_protect
def nginx_configuration_interface(request):
    if request.is_ajax():
        if request.method == 'POST':
            print "POST"
            print request.POST
        return render_to_response("test_page.html", {"test_text" : request.POST}, context_instance=RequestContext(request))
        # else:
        #     return render_to_response("test_page.html", {"test_text" : "Unknown error"}, context_instance=RequestContext(request))
    else:
        response = load_config()
        if response[0] == 0:
            result = response[1]
            return render_to_response(
                "nginx_manager/nginx_configuration_interface.html",
                result,
                context_instance=RequestContext(request),
            )
        else:
            return render_to_response(
                "nginx_manager/nginx_configuration_interface.html",
                {"nginx_conf_location": "unknown"},
                context_instance=RequestContext(request),
            )

@login_required
@csrf_protect
def nginx_configuration_editor(request):
    config_rw = NginxConfigRW()
    if request.method == "POST":
        text = request.POST.get("nginx_config_text", "unknown");
        if text != "unknown":
            config_rw.write(constant.DEFAULT_NGINX_LOCATION, text)
            response = {}
            response["nginx_config_text"] = text
            response["nginx_conf_location"] = constant.DEFAULT_NGINX_LOCATION
            return render_to_response(
                    "nginx_manager/nginx_configuration_editor.html",
                    response,
                    context_instance=RequestContext(request),
                )
        else:
            return render_to_response(
                    "nginx_manager/nginx_configuration_editor.html",
                    {}, #TODO need add params
                    context_instance=RequestContext(request),
                )

    else:
        response = {}
        response["nginx_config_text"] = config_rw.read(constant.DEFAULT_NGINX_LOCATION)
        response["nginx_conf_location"] = constant.DEFAULT_NGINX_LOCATION
        return render_to_response(
                "nginx_manager/nginx_configuration_editor.html",
                response,
                context_instance=RequestContext(request),
            )

