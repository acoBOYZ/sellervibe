from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from social_core.backends.google import GoogleOAuth2
from django.urls import reverse
from django.views.generic import View
from base.social import create_user_with_profile_picture

CustomUser = get_user_model()


@unauthenticated_user
def get_started(request):
    return render(request, 'get_started/index.html')


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/tools/mail')
        else:
            messages.warning(request, f'SALAK {email}')

    return render(request, 'login/index.html')


from .forms import V3CaptchaForm
@unauthenticated_user
def signup_page(request):
    def return_context(context={}):
        return render(request, 'signup/index.html', context)
    
    if request.method == 'POST':
        form = V3CaptchaForm(request.POST)
        if form.is_valid():
            recaptcha_score = form.cleaned_data['captcha']
            print('recaptcha_score:', recaptcha_score)

            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                validate_email(email)
            except ValidationError:
                return return_context({'error': 'Invalid email format', 'form': form})

            try:
                user = CustomUser.objects.get(email=email)
                if user is not None:
                    return return_context({'error': 'This email already in use.', 'form': form})
            except CustomUser.MultipleObjectsReturned:
                return return_context({'error': 'This email used twice. Please contact use from support', 'form': form})

            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/tools/mail')
            else:
                return return_context({'error': 'Unable to create user account', 'form': form})
        else:
            print('form.errors', form.errors)
            return return_context({'error': form.errors, 'form': form})

    form = V3CaptchaForm()
    return return_context({'form': form})


@login_required(login_url='/signup')
def logout_page(request):

    user = CustomUser.objects.filter(email=request.user).order_by('id').first()
    if user:
        logout(request)

    return redirect('/')


class GoogleLoginView(View):
    def get(self, request):
        backend = GoogleOAuth2
        scope = ['email', 'profile', 'openid']
        redirect_uri = request.build_absolute_uri(reverse('google-auth-complete'))
        authorization_url = backend.auth_url(request=request, redirect_uri=redirect_uri, scope=scope)
        return redirect(authorization_url)

class GoogleAuthCompleteView(View):
    def get(self, request):
        backend = GoogleOAuth2
        redirect_uri = request.build_absolute_uri(reverse('google-auth-complete'))
        response = backend.auth_complete(request=request, redirect_uri=redirect_uri)
        if response and response.get('user'):
            user = authenticate(request=request, uid=response.get('user').get('email'))
            if user is not None:
                if user.provider == 'google-oauth2':
                    login(request, user)
                    return redirect('/tools/mail')
                else:
                    return redirect('/signup', {'error': 'This user has an account. But not registered from google!'})
            else:
                create_user_with_profile_picture(user, response)
                return redirect('/tools/mail')
        messages.warning(request, f'Unable to authenticate with Google.')
        return redirect('/login')