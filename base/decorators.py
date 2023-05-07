from django.shortcuts import render
from functools import wraps
from django.urls import resolve
import os

def limit_functionality_if_low_score(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.recaptcha_score_is_valid:
            context = {
                'recaptcha_site_key': os.getenv('V2_RECAPTCHA_PUBLIC_KEY'),
                'view_name': resolve(request.path_info).url_name
            }
            return render(request, '../templates/slow-down.html', context)

        return view_func(request, *args, **kwargs)
    return _wrapped_view