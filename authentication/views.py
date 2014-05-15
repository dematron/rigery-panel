from django.shortcuts import RequestContext, render_to_response, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@csrf_protect
def sign_in(request):
    if "username" in request.POST and "password" in request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render_to_response("login.html",
                                      {"access_denied": "Access denied", "access_denied_class":"access_denied_text"},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response("login.html", context_instance=RequestContext(request))

@login_required
def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect("/")