from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox
import os
from django.conf import settings

class V2CheckboxReCaptchaField(ReCaptchaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, widget=ReCaptchaV2Checkbox, public_key=os.getenv('V2_RECAPTCHA_PUBLIC_KEY'), private_key=os.getenv('V2_RECAPTCHA_PRIVATE_KEY'), **kwargs)

class V3ReCaptchaField(ReCaptchaField):
    def __init__(self, *args, **kwargs):
        required_score = kwargs.pop('required_score', settings.RECAPTCHA_V3_THRESHOLD)
        super().__init__(*args, widget=ReCaptchaV3(attrs={'required_score': required_score}), public_key=os.getenv('V3_RECAPTCHA_PUBLIC_KEY'), private_key=os.getenv('V3_RECAPTCHA_PRIVATE_KEY'), **kwargs)
