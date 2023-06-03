from functools import wraps
import os
from django.http import JsonResponse

def is_user_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return JsonResponse({'success': False, 'error': 'Login required'})
    return _wrapped_view

def is_user_authenticated_and_autolead_creator(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_autoleads_creator and request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return JsonResponse({'success': False, 'error': 'You are not a creator!'})
    return _wrapped_view