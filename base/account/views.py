from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


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

#acvdtozturk@gmail.com
@unauthenticated_user
def signup_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        context = {}

        try:
            validate_email(email)
        except ValidationError:
            print('Invalid email format')
            context['error'] = 'Invalid email format'
            return render(request, 'signup/index.html', context)
        
        print('email is valid')

        if User.objects.filter(username=email).exists():
            context['error'] = 'Email already exists'
            return render(request, 'signup/index.html', context)

        if password1 != password2:
            context['error'] = 'Passwords do not match'
            return render(request, 'signup/index.html', context)

        # user = User.objects.create_user(username=email, email=email, password=password1)
        # user = authenticate(request, username=email, password=password1)

        # if user is not None:
        #     login(request, user)
        #     return redirect('/tools/mail')
        # else:
        #     context['error'] = 'Unable to create user account'
        #     return render(request, 'signup/index.html', context)

    return render(request, 'signup/index.html')

@login_required(login_url='/signup')
def logout_page(request):
    logout(request)
    return redirect('/')
