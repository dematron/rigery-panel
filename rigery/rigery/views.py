__author__ = 'alexey'

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

#переадресация на страницу идентификации при неизвестном пользователе
@login_required
def test_response(request):
    return render_to_response('base.html')

def sign_in(request):
    return render_to_response('authentication.html')