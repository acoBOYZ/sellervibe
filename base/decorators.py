from django.shortcuts import render
from functools import wraps
from django.urls import resolve
import os
from django.http import JsonResponse
from .forms import V3CaptchaForm

def limit_functionality_if_low_score(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.form = V3CaptchaForm(request.POST)
        request.recaptcha_score_is_valid = request.form.is_valid() if request.method == 'POST' else True
        if not request.recaptcha_score_is_valid:
            context = {
                'recaptcha_site_key': os.getenv('V2_RECAPTCHA_PUBLIC_KEY'),
                'view_name': resolve(request.path_info).url_name
            }
            return render(request, '../templates/slow-down.html', context)

        return view_func(request, *args, **kwargs)
    return _wrapped_view

def is_user_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Login required'})
        return view_func(request, *args, **kwargs)
    return _wrapped_view