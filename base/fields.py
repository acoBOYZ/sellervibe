from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

class V3ReCaptchaField(ReCaptchaField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, widget=ReCaptchaV3, required=False, **kwargs)