from django.utils.deprecation import MiddlewareMixin
from .forms import V3CaptchaForm

class ReCaptchaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.form = V3CaptchaForm(request.POST)
        request.recaptcha_score_is_valid = request.form.is_valid() if request.method == 'POST' else True
        return None