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

from base.forms import V3CaptchaForm
from base.decorators import limit_functionality_if_low_score

CustomUser = get_user_model()

def getIndexHtml(index):
    return f'../templates/account/{index}/index.html'


@unauthenticated_user
def getStarted(request):
    return render(request, getIndexHtml('get-started'))


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/tools/mail')
        else:
            messages.warning(request, f'SALAK {email}')

    return render(request, getIndexHtml('login'))


@unauthenticated_user
@limit_functionality_if_low_score
def signupPage(request):
    def return_context(context={}):
        return render(request, getIndexHtml('signup'), context)
    
    if request.method == 'POST':
        if request.recaptcha_score_is_valid:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                validate_email(email)
            except ValidationError:
                return return_context({'error': 'Invalid email format', 'form': request.form})

            if CustomUser.objects.filter(email=email).exists():
                return return_context({'error': 'This email already in use.', 'form': request.form})

            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/tools/mail')
            else:
                return return_context({'error': 'Unable to create user account', 'form': request.form})
        else:
            print('form.errors', request.form.errors)
            return return_context({'error': request.form.errors, 'form': request.form})

    return return_context({'form': request.form})


@login_required(login_url='/signup')
def logoutPage(request):

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