from django.shortcuts import render
import os
import requests
from django.http import JsonResponse

def slowDown(request):
    context = {
        'recaptcha_site_key': os.getenv('HECAPTCHA_PUBLIC_KEY'),
        'view_name': 'slow-down'
    }
    return render(request, '../templates/slow-down.html', context)

def verify_hcaptcha(request):
    if request.method == 'POST':
        hcaptcha_token = request.POST.get('hcaptcha-token')
        if not hcaptcha_token:
            return JsonResponse({'success': False, 'error': 'No hCaptcha token'})
        data = {
            'response': hcaptcha_token,
            'secret': os.getenv('HECAPTCHA_PRIVATE_KEY'),
        }
        session = requests.session()
        with session.post('https://hcaptcha.com/siteverify', data=data) as response:
            if response.status_code == 200:
                response_json = response.json()

                if response_json['success']:
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'error': response_json['error-codes']})

    return JsonResponse({'success': False, 'error': 'Request method is not valid'})