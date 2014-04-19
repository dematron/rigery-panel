__author__ = 'alexey'

from django.shortcuts import render_to_response

def test_response(request):
    return render_to_response('base.html')