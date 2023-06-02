from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import authenticated_user

from social_core.backends.google import GoogleOAuth2
from django.urls import reverse
from django.views.generic import View
from base.social import create_user_with_profile_picture
import os
import requests

CustomUser = get_user_model()

def getIndexHtml(index):
    return f'../templates/account/{index}/index.html'

@authenticated_user
def getStarted(request):
    return render(request, getIndexHtml('get-started'))


@authenticated_user
def loginPage(request):
    def return_context(context={}):
        return render(request, getIndexHtml('login'), context)

    context = {
        'hecaptcha_site_key': os.getenv('HECAPTCHA_PUBLIC_KEY'),
        'view_name': 'slow-down'
    }

    if request.method == 'POST':
        token = request.POST.get('h-captcha-response')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if token:
            data = { 'secret': os.getenv('HECAPTCHA_PRIVATE_KEY'), 'response': token }
            session = requests.session()
            with session.post('https://hcaptcha.com/siteverify', data=data) as response:
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json['success']:
                        user = CustomUser.objects.authenticate_user(email=email, password=password)
                        if user is not None:
                            login(request, user)
                            return redirect('/tools/mail')
                        else:
                            context['error'] = 'Email or password is incorrect.'
                    else:
                        context['error'] = 'Please check your network connection and try again.'
                else:
                    context['error'] = 'Please try again with solve hcaptcha.'

        else:
            context['error'] = 'Something went wrong. Please try again with solve hcaptcha.'

        context['email'] = email
        context['password'] = password

    return return_context(context)


@authenticated_user
def signupPage(request):
    def return_context(context={}):
        return render(request, getIndexHtml('signup'), context)
    
    context = {
        'hecaptcha_site_key': os.getenv('HECAPTCHA_PUBLIC_KEY'),
        'view_name': 'slow-down'
    }

    if request.method == 'POST':
        token = request.POST.get('h-captcha-response')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if token:
            data = { 'secret': os.getenv('HECAPTCHA_PRIVATE_KEY'), 'response': token }
            session = requests.session()
            with session.post('https://hcaptcha.com/siteverify', data=data) as response:
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json['success']:
                        user = CustomUser.objects.create_and_authenticate_user(username=username, email=email, password=password)
                        if user is not None:
                            login(request, user)
                            return redirect('/tools/mail')
                        else:
                            context['error'] = 'Unable to create user account'
                    else:
                        context['error'] = 'Please check your network connection and try again.'
        else:
            context['error'] = 'Something went wrong. Please try again with solve hcaptcha.'

        
        context['username'] = username
        context['email'] = email
        context['password'] = password

    return return_context(context)


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
