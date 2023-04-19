from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.views.decorators.csrf import csrf_exempt
from openpyxl import load_workbook
import csv
from django.http import JsonResponse

def mail(request):
    return render(request, 'mail/index.html')

def contacts(request):
    return render(request, 'contacts/index.html')

def templates(request):
    return render(request, 'templates/index.html')

def send(request):
    return render(request, 'send/index.html')

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            file_path = os.path.join(f'{file.name}')
            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            emails = []
            if file.name.endswith('.xlsx'):
                wb = load_workbook(file_path)
                ws = wb.active
                header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))
                email_column = None
                for i, header in enumerate(header_row):
                    if header == 'email':
                        email_column = i + 1
                        break
                if email_column is None:
                    return JsonResponse({'success': False, 'error': 'Email column not found'})
                for row in ws.iter_rows(min_row=2, values_only=True):
                    email = row[email_column - 1]
                    if email:
                        emails.append(email)
            elif file.name.endswith('.csv'):
                delimiter = ','
                with open(file_path, newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=delimiter)
                    header_row = next(reader)
                    email_column = None
                    for i, header in enumerate(header_row):
                        if header == 'email':
                            email_column = i
                            break
                    if email_column is None:
                        return JsonResponse({'success': False, 'error': 'Email column not found'})
                    emails = []
                    for row in reader:
                        email = row[email_column]
                        if email:
                            emails.append(email)
            else:
                return JsonResponse({'success': False, 'error': 'Unsupported file type'})
            os.remove(file_path)
            return JsonResponse({'success': True, 'emails': emails})
    return JsonResponse({'success': False})

from django.contrib.auth.models import User
from tool_mail.models import UserJSON

@csrf_exempt
def save_file(request):
    if request.method == 'POST':
        jsFile = request.FILES.get('file')
        if jsFile:
            user = User.objects.get(username=request.user)
            json_data = jsFile['data']
            user_json = UserJSON(user=user, name=jsFile['name'], json_file=json_data)
            user_json.save()


@csrf_exempt
def get_file(request):
    if request.method == 'GET':
        name = request.get('name')
        if name:
            user = User.objects.get(username=request.user)
            user_json = UserJSON.objects.get(user=user, name=name)
            json_data = user_json.json_file
            return JsonResponse(json_data)