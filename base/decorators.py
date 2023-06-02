from functools import wraps
import os
from django.http import JsonResponse

def is_user_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Login required'})
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def is_user_autolead_creator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_autoleads_creator:
            return JsonResponse({'success': False, 'error': 'Login required'})
        return view_func(request, *args, **kwargs)
    return _wrapped_view