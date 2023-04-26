from django.shortcuts import render
import os
from django.views.decorators.csrf import csrf_exempt
from openpyxl import load_workbook
import csv
from django.http import JsonResponse
import re
from django.contrib.auth.decorators import login_required
from .models import UserEmails
import json
from django.db.models import Q

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
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'})
        file = request.FILES.get('file')
        if file:

            def validate_email(email):
                regex = r'\S+@\S+\.\S+'
                return bool(re.match(regex, email))
            
            file_path = os.path.join(f'{file.name}')
            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            emails = []
            total_count = 0
            validate_count = 0
            if file.name.endswith('.xlsx'):
                wb = load_workbook(file_path)
                ws = wb.active
                header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))
                name_column = None
                title_column = None
                email_column = None
                status_column = None
                for i, header in enumerate(header_row):
                    _header = str(header).lower()
                    if name_column is None and _header == 'name':
                        name_column = i + 1
                    elif title_column is None and _header == 'title':
                        title_column = i + 1
                    elif email_column is None and _header == 'email':
                        email_column = i + 1
                    elif status_column is None and _header == 'status':
                        status_column = i + 1
                if email_column is None:
                    return JsonResponse({'success': False, 'error': 'Email column not found'})
                for row in ws.iter_rows(min_row=2, values_only=True):
                    email = {'name': row[name_column - 1] if name_column is not None else '',
                             'title': row[title_column - 1] if title_column is not None else '',
                             'email': row[email_column - 1],
                             'status': (row[status_column - 1] == 'true') if status_column is not None else True}
                    total_count += 1
                    if email['email'] and validate_email(email['email']):
                        emails.append(email)
                        validate_count += 1
            else:
                return JsonResponse({'success': False, 'error': 'Unsupported file type'})
            os.remove(file_path)
            return JsonResponse({'success': True, 'emails': emails, 'total_count': total_count, 'validate_count': validate_count, 'unknown_count': total_count - validate_count})
    return JsonResponse({'success': False})

@login_required
def get_email_names(request):
    email_file_names = UserEmails.objects.filter(user=request.user).values_list('name', flat=True).distinct()
    return JsonResponse({'names': list(email_file_names)})

@login_required
@csrf_exempt
def save_emails(request):
    if request.method == 'POST':
        emails = json.loads(request.POST.get('emails'))
        delete_all = len(emails) == 0
        name = request.POST.get('name')
        user_emails = UserEmails.objects.filter(user=request.user, name=name)
        user_emails.delete()
        if not delete_all:
            user_emails = UserEmails(user=request.user, name=name, emails=emails)
            user_emails.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def get_emails(request):
    name = request.GET.get('name') or request.POST.get('name')
    queryset = UserEmails.objects.filter(user=request.user)
    if name:
        queryset = queryset.filter(name=name)
    emails = queryset.values_list('emails', flat=True).distinct()
    return JsonResponse({'success': True, 'emails': list(emails)}, safe=False)
