from django.db import models
from django.forms.models import model_to_dict
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
import re
import os
from pathlib import Path
from django.conf import settings
from openpyxl import load_workbook
from unidecode import unidecode
from django.utils import timezone
import json
import subprocess
import psutil

class App(models.Model):
    name = models.CharField(_('App name'), max_length=100, unique=True)
    created_by = models.EmailField(_('Created by'), default='')
    created_time = models.DateTimeField(_('Date created'), default=timezone.now)
    edited_by = models.EmailField(_('Edited by'), default='')
    edited_time = models.DateTimeField(_('Date edited'), default=timezone.now)
    black_list = models.TextField(_('Black list'), default='amazon, ebay')
    loop_time = models.CharField(_('Loop time'), max_length=10, default='60')
    amazon_base_url = models.URLField(_('Amazon base URL'), max_length=200, default='https://www.amazon.com/dp/')
    compare_value = models.CharField(_('Compare value'), max_length=10, default='35')
    auto_restart_value = models.BooleanField(_('Auto restart'), default=True)
    force_restart_count = models.CharField(_('Force restart count'), max_length=10, default='0')
    auto_restart_count = models.CharField(_('Auto restart count'), max_length=10, default='0')
    
    def __str__(self):
        return self.name

    @classmethod
    @transaction.atomic
    def create_or_update_multiple(cls, user, bulk_data):
        try:
            for data in bulk_data:
                excluded_keys = {'proxy_settings', 'webhooks', 'amazon_products'}
                defaults = {k: v for k, v in data.items() if k not in excluded_keys}
                defaults.update({"edited_by": user.email, "edited_time": timezone.now()})
                app_item, created = cls.objects.update_or_create(
                    name=data.get('name'),
                    defaults=defaults
                )

                proxy_data_list = data.get('proxy_settings', [])
                proxy_api_keys = [proxy_data.get('api_key') for proxy_data in proxy_data_list]
                ProxySetting.objects.filter(app=app_item).exclude(api_key__in=proxy_api_keys).delete()
                for proxy_data in proxy_data_list:
                    ProxySetting.objects.update_or_create(
                        app=app_item,
                        api_key=proxy_data.get('api_key'),
                        defaults=proxy_data
                    )

                webhook_data_list = data.get('webhooks', [])
                webhook_names = [webhook_data.get('name') for webhook_data in webhook_data_list]
                Webhook.objects.filter(app=app_item).exclude(name__in=webhook_names).delete()
                for webhook_data in webhook_data_list:
                    Webhook.objects.update_or_create(
                        app=app_item,
                        name=webhook_data.get('name'),
                        defaults=webhook_data
                    )

                amazon_product_data_list = data.get('amazon_products', [])
                product_ASINs = [amazon_product_data.get('ASIN') for amazon_product_data in amazon_product_data_list]
                AmazonProduct.objects.filter(app=app_item).exclude(ASIN__in=product_ASINs).delete()
                for amazon_product_data in amazon_product_data_list:
                    AmazonProduct.objects.update_or_create(
                        app=app_item,
                        ASIN=amazon_product_data.get('ASIN'),
                        defaults=amazon_product_data
                    )

                return {'success': True, 'message': 'App data updated/created successfully.'}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    @classmethod
    def get_all(cls, user):
        try:
            app_items = cls.objects.all().prefetch_related('proxy_settings', 'webhooks', 'amazon_products')
            if app_items.exists():
                data = []
                for app in app_items:
                    app_data = model_to_dict(app)
                    app_data.pop('id', None)
                    app_data.pop('created_by', None)
                    app_data.pop('created_time', None)
                    app_data.pop('edited_by', None)
                    app_data.pop('edited_time', None)
                    app_data.pop('force_restart_count', None)
                    app_data.pop('auto_restart_count', None)
                    
                    app_data['proxy_settings'] = []
                    for proxy in app.proxy_settings.all():
                        proxy_data = model_to_dict(proxy)
                        proxy_data.pop('id', None)
                        proxy_data.pop('app', None)
                        proxy_data.pop('app_id', None)
                        app_data['proxy_settings'].append(proxy_data)

                    app_data['webhooks'] = []
                    for webhook in app.webhooks.all():
                        webhook_data = model_to_dict(webhook)
                        webhook_data.pop('id', None)
                        webhook_data.pop('app', None)
                        webhook_data.pop('app_id', None)
                        app_data['webhooks'].append(webhook_data)

                    app_data['amazon_products'] = []
                    for product in app.amazon_products.all():
                        product_data = model_to_dict(product)
                        product_data.pop('id', None)
                        product_data.pop('app', None)
                        app_data['amazon_products'].append(product_data)

                    data.append(app_data)
                return {'success': True, 'data': data}

            default_app = cls.objects.create(name="Default App", created_by=user, edited_by=user)
            ProxySetting.objects.create(app=default_app, server_name="scrapedo", api_key="")
            Webhook.objects.create(app=default_app, name="default", config={})

            default_app_data = list(cls.objects.filter(id=default_app.id).prefetch_related('proxy_settings', 'webhooks', 'amazon_products').values())
            return {'success': True, 'data': default_app_data}

        except Exception as e:
            return {'success': False, 'error': str(e)}

class ProxySetting(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='proxy_settings')
    cls_name = 'Proxy Settings'
    server_name = models.CharField(_('Server name'), max_length=30, default='scrapedo')
    api_key = models.CharField(_('Api key'), max_length=100, default='')
    concurrent_requests_limit = models.CharField(_('Concurrent requests limit'), max_length=30, default='5')
    timeout_value = models.CharField(_('Timeout value'), max_length=30, default='30')

class Webhook(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='webhooks')
    cls_name = 'Webhook Designer'
    name = models.CharField(_('Webhook name'), max_length=100)
    config = models.JSONField(_('Config'), default=None)

class AmazonProduct(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='amazon_products')
    cls_name = 'Amazon Products'
    ASIN = models.CharField(_('ASIN'), max_length=10, unique=True)
    UPCS = models.TextField(_('UPCS'), default='')
    status = models.BooleanField(_('Status'), default=True)

class AppService:
    @staticmethod
    def set_all(user, apps):
        if not apps:
            response = {'success': False, 'error': 'Data is not available'}

        response = App.create_or_update_multiple(user, apps)
        if response['success']:
            APP_DIR = Path(__file__).resolve().parent
            with open(os.path.join(APP_DIR, 'app/apps.json'), 'w') as f:
                json.dump(apps, f)
        return JsonResponse(response)
        
    @staticmethod
    def get_all(user):
        apps = App.get_all(user=user)
        return JsonResponse({'success': True, 'data': apps})



class AuxiliaryService:
    @staticmethod
    def check_if_script_is_running(script_name):
        for process in psutil.process_iter():
            try:
                for cmd in process.cmdline():
                    if script_name in cmd:
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    @staticmethod
    def read_json_file(filename):
        content = ...
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except:
            return None
        return json.loads(content)
    
    @staticmethod
    def get_info_script():
        try:
            APP_DIR = Path(__file__).resolve().parent
            json_path = os.path.join(APP_DIR, 'app/running.app')

            data = AuxiliaryService.read_json_file(json_path)
            if data:
                return JsonResponse({'success': True, 'data': data})
            return JsonResponse({'success': False, 'error': 'Can not read script data yet!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'An error occurred while getting script info: {str(e)}'})
        
    @staticmethod
    def force_restart_script(user):
        try:
            APP_DIR = Path(__file__).resolve().parent
            script_path = os.path.join(APP_DIR, 'app/main.py')
            if AuxiliaryService.check_if_script_is_running(script_path):
                if settings.IS_SERVER:
                    subprocess.Popen(["sudo", "/bin/systemctl", "restart", "autoleads_app"])
                else:
                    with open(os.path.join(APP_DIR, 'app/restart.app'), 'w') as f:
                        pass

                return JsonResponse({'success': True, 'message': 'App succesfuly restarted.'})
            return JsonResponse({'success': False, 'error': 'The app needs to be start first.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'An error occurred while force restart: {str(e)}'})
        
    @staticmethod
    def force_start_script(user):
        try:
            APP_DIR = Path(__file__).resolve().parent
            venv_python_path = os.path.join(settings.BASE_DIR, '.venv/bin/python')
            script_path = os.path.join(APP_DIR, 'app/main.py')
            if not AuxiliaryService.check_if_script_is_running(script_path):
                json_path = os.path.join(APP_DIR, 'app/running.app')
                data = AuxiliaryService.read_json_file(json_path)
                if data:
                    if data['running']:
                        return JsonResponse({'success': False, 'error': 'The app already running.'})
                    else:
                        if settings.IS_SERVER:
                            subprocess.Popen(["sudo", "/bin/systemctl", "start", "autoleads_app"])
                        else:
                            subprocess.Popen([venv_python_path, script_path])
                else:
                    if settings.IS_SERVER:
                        subprocess.Popen(["sudo", "/bin/systemctl", "start", "autoleads_app"])
                    else:
                        subprocess.Popen([venv_python_path, script_path])
            else:
                return JsonResponse({'success': False, 'error': 'The app already running.'})

            return JsonResponse({'success': True, 'message': 'The app succesfuly started.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'An error occurred while force restart: {str(e)}'})

    @staticmethod
    def upload_product_files(user, files):
        if not files:
            return JsonResponse({'success': False, 'error': 'Files not found'})
        
        def validate_asin(asin):
            asin_regex = r'^[a-zA-Z0-9]{10}$'
            return re.match(asin_regex, str(asin)) is not None
        
        def remove_file(file_path):
            if os.path.exists(file_path):
                os.remove(file_path)

        user_folder_dir = os.path.join(settings.MEDIA_ROOT, str(user))
        if not os.path.exists(user_folder_dir):
            os.makedirs(user_folder_dir)

        file_errors = {'success': False, 'error': ''}
        file_paths = []
        for file in files:
            file_path = os.path.join(user_folder_dir, f'{file.name}')
            try:
                with open(file_path, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                file_paths.append(file_path)
            except Exception as e:
                file_errors['error'] += f'{e}\t'
        
        if not file_paths:
            return JsonResponse(file_errors)
                
        products = []
        total_count = 0
        validate_count = 0
        MAX_PRODUCT_COUNT = 1000
        error_responses = ''

        try:
            for file in files:
                if file.name.endswith('.xlsx'):
                    wb = load_workbook(file_path)
                    ws = wb.active
                    header_row = next(ws.iter_rows(min_row=0, max_row=3, values_only=True))
                    asin_column = None
                    upc_column = None
                    for i, header in enumerate(header_row):
                        _header = unidecode(str(header)).strip().upper().replace(' ', '_')
                        if _header == 'none':
                            continue
                        if asin_column is None and ('ASIN' in _header):
                            asin_column = i + 1
                        elif  upc_column is None and ('UPC' in _header):
                            upc_column = i + 1

                    if asin_column is None:
                        for row in ws.iter_rows(min_row=0, max_row=3, values_only=True):
                            for i, cell_value in enumerate(row):
                                if validate_asin(cell_value):
                                    asin_column = i + 1
                                    break

                    if asin_column is None:
                        remove_file(file_path)
                        error_responses += f'In {file.name} asin column not found\t'

                    if asin_column is None:
                        continue

                    seen_asins = set()
                    for row in ws.iter_rows(min_row=2, values_only=True):
                        if len(seen_asins) >= MAX_PRODUCT_COUNT:
                            break
                        asin = row[asin_column - 1]
                        if asin is None or asin in seen_asins:
                            continue
                        seen_asins.add(asin)
                        total_count += 1
                        if asin and validate_asin(asin):
                            asin_data = {'ASIN': asin}
                            if upc_column is not None:
                                asin_data['UPCS'] = row[upc_column - 1]
                            asin_data['status'] = True
                            products.append(asin_data)
                            validate_count += 1
                else:
                    remove_file(file_path)
                    return {'success': False, 'error': 'Unsupported file type'}
        except Exception as e:
            remove_file(file_path)
            return {'success': False, 'error': f'An error occurred: {str(e)}'}
        finally:
            remove_file(file_path)
        return {'success': True, 'products': products, 'total_count': total_count, 'validate_count': validate_count, 'unknown_count': total_count - validate_count}
