from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

def mail(request):
    return render(request, 'mail/index.html')
