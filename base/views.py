from django.shortcuts import render
import os

def slowDown(request):
    context = {
        'recaptcha_site_key': os.getenv('V2_RECAPTCHA_PUBLIC_KEY'),
        'view_name': 'slow-down'
    }
    return render(request, '../templates/slow-down.html', context)