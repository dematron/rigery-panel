__author__ = 'kutepoval'

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import *

@login_required
def test_nginx(request):
    return render_to_response("servers/nginx_configuration.html")

@login_required
def test_response(request):
    return render_to_response("index.html")
