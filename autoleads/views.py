from django.shortcuts import render
import os
from pathlib import Path
from django.http import JsonResponse
from .models import AuxiliaryService, AppService
import json
from base.decorators import is_user_authenticated, is_user_autolead_creator
from account.decorators import unauthenticated_user, unauthenticated_user_is_autolead_creator

def getIndexHtml(index):
    context = { }
    return f'../templates/autoleads/{index}/index.html', context

@unauthenticated_user
def dashboard(request):
    def return_context(context={}):
        return render(request, getIndexHtml('dashboard'), context)
    return return_context({'form': request})

@unauthenticated_user
@unauthenticated_user_is_autolead_creator
def creator(request):
    def return_context(context={}):
        return render(request, getIndexHtml('creator'), context)
    
    try:
        APP_DIR = Path(__file__).resolve().parent
        with open(os.path.join(APP_DIR, 'app/selector.json'), 'r') as f:
            content = f.read()
        fields = json.loads(content)
        
        context = {
            'hecaptcha_site_key': os.getenv('HECAPTCHA_PUBLIC_KEY'),
            'view_name': 'slow-down',
            'fields': fields
        }
    except Exception as e:
        context = {
            'hecaptcha_site_key': os.getenv('HECAPTCHA_PUBLIC_KEY'),
            'view_name': 'slow-down',
            'error': str(e)
        }
    return return_context(context)

@is_user_authenticated
@is_user_autolead_creator
def upload_product_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('attachment')
        if files:
            result = AuxiliaryService.upload_product_files(request.user, files)
            return JsonResponse(result)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
@is_user_autolead_creator
def get_or_set_all_apps(request):
    if request.method == 'GET':
        return AppService.get_all(user=request.user)
    elif request.method == 'POST':
        apps = json.loads(request.POST.get('apps'))
        return AppService.set_all(user=request.user, apps=apps)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
@is_user_autolead_creator
def force_restart_to_app(request):
    if request.method == 'POST':
        return AuxiliaryService.force_restart_script(user=request.user)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
@is_user_autolead_creator
def get_info_from_app(request):
    if request.method == 'GET':
        return AuxiliaryService.get_info_script()
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
@is_user_autolead_creator
def force_start_to_app(request):
    if request.method == 'POST':
        return AuxiliaryService.force_start_script(user=request.user)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})