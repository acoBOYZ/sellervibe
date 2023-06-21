from django.shortcuts import render
import os
from pathlib import Path
from django.http import JsonResponse
from .models import AuxiliaryService, AppService
from django.views.decorators.csrf import csrf_exempt
import json
from base.decorators import is_user_authenticated_and_autolead_creator
from account.decorators import authenticated_user_is_autolead_creator, unauthenticated_user
from django.http import HttpResponse
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async

def getIndexHtml(index):
    context = { }
    return f'../templates/autoleads/{index}/index.html', context

@unauthenticated_user
def dashboard(request):
    def return_context(context={}):
        return render(request, getIndexHtml('dashboard'), context)
    return return_context({'form': request})

@authenticated_user_is_autolead_creator
def creator(request):
    def return_context(context={}):
        return render(request, getIndexHtml('creator'), context)

    context = {
        'hecaptcha_site_key': os.getenv('HECAPTCHA_PUBLIC_KEY'),
        'view_name': 'slow-down',
        'fields': None
    }
    try:
        APP_DIR = Path(__file__).resolve().parent
        selectorFilePath = os.path.join(APP_DIR, 'app/selector.json')
        if os.path.exists(selectorFilePath):
            with open(selectorFilePath, 'r') as f:
                content = f.read()
            fields = json.loads(content)
            
            context['fields'] = fields
    except:
        pass
    return return_context(context)

@is_user_authenticated_and_autolead_creator
def upload_product_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('attachment')
        if files:
            result = AuxiliaryService.upload_product_files(request.user, files)
            return JsonResponse(result)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated_and_autolead_creator
def get_or_set_all_apps(request):
    if request.method == 'GET':
        response = AppService.get_all(user=request.user)
        return JsonResponse(response)
    elif request.method == 'POST':
        apps = json.loads(request.POST.get('apps'))
        response = AppService.set_all(user=request.user, apps=apps)
        return JsonResponse(response)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

# @is_user_authenticated_and_autolead_creator
# def force_restart_to_app(request):
#     if request.method == 'POST':
#         return AuxiliaryService.force_restart_script(user=request.user)
#     return JsonResponse({'success': False, 'error': 'Request method is not valid'})

# @is_user_authenticated_and_autolead_creator
# def get_info_from_app(request):
#     if request.method == 'GET':
#         return JsonResponse(AuxiliaryService.get_info_script())
#     return JsonResponse({'success': False, 'error': 'Request method is not valid'})

# @is_user_authenticated_and_autolead_creator
# def force_start_to_app(request):
#     if request.method == 'POST':
#         return AuxiliaryService.force_start_script(user=request.user)
#     return JsonResponse({'success': False, 'error': 'Request method is not valid'})


# @csrf_exempt
# async def webhook(request, token):
#     try:
#         webhook = await database_sync_to_async(WebHook.objects.get)(token=token)
#     except WebHook.DoesNotExist:
#         return HttpResponse({'status':'Failed'}, status=404)
    
#     if request.method == 'POST':
#         data = await sync_to_async(request.body.decode)()
#         json_data = json.loads(data)
        
#         # Asynchronous operations can be done here
        
#         return HttpResponse({'status':'OK'}, status=200)
#     else:
#         return HttpResponse({'status':'Failed'}, status=405)