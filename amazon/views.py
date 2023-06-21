from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import ProductService
from django.http import HttpResponse, JsonResponse
from asgiref.sync import async_to_sync
import json

# @csrf_exempt
# async def amazon_fetch(request):
#     pass

# @csrf_exempt
# def amazon_create_all(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))
#         if 'command' in data and 'products' in data:
#             command = data.get('command')
#             if command == 'create_all':
#                 async_to_sync(ProductService.bulk_create_or_update)(data.get('products', []))
#         return HttpResponse(status=200)
#     return HttpResponse(status=403)


# @csrf_exempt
# def get_all_from_discord(request):
#     if request.method == 'GET':
#         data = ProductService.get_all_data_for_discord()
#         return JsonResponse({'success': True, 'data': data})
#     return JsonResponse({'success': False, 'error': 'Request method is not valid'})