from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import UserEmails, UserTemplates
import json
from base.decorators import limit_functionality_if_low_score, is_user_authenticated
import os

def getIndexHtml(index):
    context = { 
        'recaptcha_site_key': os.getenv('V3_RECAPTCHA_PUBLIC_KEY'), 
        'recaptcha_action': f'emailForm_{index}'
        }
    return f'../templates/email-tool/{index}/index.html', context

def start(request):
    index, context = getIndexHtml('start')
    return render(request, index, context)

def contacts(request):
    index, context = getIndexHtml('contacts')
    return render(request, index, context)

def templates(request):
    index, context = getIndexHtml('templates')
    return render(request, index, context)

def send(request):
    index, context = getIndexHtml('send')
    return render(request, index, context)

@is_user_authenticated
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            result = UserEmails.process_email_file(request.user, file)
            return JsonResponse(result)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
def get_email_names(request):
    if request.method == 'POST':
        result = UserEmails.get_all_email_names(request.user)
        return JsonResponse(result)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
def save_emails(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        emails = json.loads(request.POST.get('emails'))
        result = UserEmails.save_emails(request.user, name, emails)
        return JsonResponse(result)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
def get_emails(request):
    if request.method == 'POST':
        name = request.GET.get('name')
        result = UserEmails.get_emails(request.user, name)
        return JsonResponse(result, safe=False)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
def upload_attachments(request):
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('attachment')
            response = UserEmails.upload_attachments(request.user, files)
            return JsonResponse(response)
        except Exception as e:
            JsonResponse({'success': False, 'error': f'An error occurred: {str(e)}'})
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
def send_bulk_emails(request):
    if request.method == 'POST':
        try:
            attachment_list = []
            email_list = []
            cc_list = []

            for attachment in request.POST.getlist('attachment'):
                attachment_list.append(attachment)
            for email in request.POST.getlist('email'):
                _e = json.loads(email)
                if _e['status']:
                    email_list.append(_e)
            if len(email_list) == 0:
                return JsonResponse({'success': False, 'error': 'email list is empty'})
            text_from = request.POST.get('from')
            text_replyTo = request.POST.get('replyTo')
            for cc in request.POST.getlist('cc'):
                cc_list.append(cc)
            text_subject = request.POST.get('subject')
            text_message = request.POST.get('message')

            email_data = {
                'attachment_list': attachment_list,
                'email_list': email_list,
                'cc_list': cc_list,
                'from': text_from,
                'replyTo': text_replyTo,
                'subject': text_subject,
                'message': text_message
            }
            
            return JsonResponse(UserEmails.send_bulk_emails_via_elasticemail(email_data))
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'An error occurred: {str(e)}'})
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
def save_template(request):    
    if request.method == 'POST':
        name = request.POST.get('name')
        template = request.POST.get('html_content')

        response = UserTemplates.save_template_content(
            user=request.user,
            name=name,
            template=template
        )
        return JsonResponse(response)
    return JsonResponse({"status": "error"})

@is_user_authenticated
def get_templates(request):
    if request.method == 'POST':
        response = UserTemplates.get_template_content(user=request.user)
        return JsonResponse(response, safe=False)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})

@is_user_authenticated
def delete_template(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        response = UserTemplates.delete_template_content(user=request.user, name=name)
        return JsonResponse(response)
    return JsonResponse({'success': False, 'error': 'Request method is not valid'})