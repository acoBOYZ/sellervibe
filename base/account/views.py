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


@unauthenticated_user
def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        context = {}

        try:
            validate_email(email)
        except ValidationError:
            context['error'] = 'Invalid email format'
            return render(request, 'signup/index.html', context)

        try:
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                return redirect('/tools/mail')
            else:
                context['error'] = 'Unable to log in'
                return render(request, 'signup/index.html', context)
        except CustomUser.DoesNotExist:
            if password1 != password2:
                context['error'] = 'Passwords do not match'
                return render(request, 'signup/index.html', context)
        except CustomUser.MultipleObjectsReturned:
            context['error'] = 'This email used twice. Please contact use from support'
            return render(request, 'signup/index.html', context)

        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user = authenticate(request, email=email, password=password1)

        if user is not None:
            login(request, user)
            return redirect('/tools/mail')
        else:
            context['error'] = 'Unable to create user account'
            return render(request, 'signup/index.html', context)

    return render(request, 'signup/index.html')


@login_required(login_url='/signup')
def logout_page(request):
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
                login(request, user)
                
                # retrieve profile picture from Google and store in user profile
                profile_picture_url = response.get('user').get('picture')
                create_user_with_profile_picture(user, response, profile_picture_url)
                
                return redirect('/tools/mail')
        messages.warning(request, f'Unable to authenticate with Google.')
        return redirect('/login')