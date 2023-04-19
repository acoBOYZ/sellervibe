from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user


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
    return render(request, 'signup/index.html')

@login_required(login_url='/signup')
def logout_page(request):
    logout(request)
    return redirect('/')
