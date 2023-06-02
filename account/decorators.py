# from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/tools/mail')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def unauthenticated_user_is_autolead_creator(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_autoleads_creator:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/autoleads/dashboard')
    return wrapper_func