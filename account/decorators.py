# from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        return view_func(request, *args, **kwargs)
    return wrapper_func

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/tools/mail')
        return view_func(request, *args, **kwargs)
    return wrapper_func

def authenticated_user_is_autolead_creator(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_autoleads_creator and request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('/autoleads/dashboard')
    return wrapper_func