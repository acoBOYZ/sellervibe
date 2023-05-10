from django import forms
from .fields import V3ReCaptchaField, V2CheckboxReCaptchaField
from django.contrib.admin.forms import AdminAuthenticationForm

class V2CheckboxCaptchaForm(forms.Form):
    captcha = V2CheckboxReCaptchaField()

class V3CaptchaForm(forms.Form):
    captcha = V3ReCaptchaField()

class V2CaptchaFormAdmin(AdminAuthenticationForm):
    captcha = V2CheckboxReCaptchaField()