__author__ = 'kutepoval'

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import *

@login_required
def test_response(request):
    return render_to_response("index.html")
