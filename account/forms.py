from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from base.fields import V3ReCaptchaField

class V3CaptchaForm(forms.Form):
    captcha = V3ReCaptchaField()