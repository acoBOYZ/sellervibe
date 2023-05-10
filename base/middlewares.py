from django.utils.deprecation import MiddlewareMixin
from .forms import V3CaptchaForm

#its an example and not using right now!
class ReCaptchaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print('middlewares_reqquest:', request)
        request.form = V3CaptchaForm(request.POST)
        request.recaptcha_score_is_valid = request.form.is_valid() if request.method == 'POST' else True
        return None