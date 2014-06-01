__author__ = 'kutepoval'

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import *
import scripts.monitoring.get_host_info as host_info



@login_required
def start_page(request):
    return render_to_response("index.html", host_info.get_host_info())
