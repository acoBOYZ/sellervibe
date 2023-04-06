from django.shortcuts import render

def get_started(request):
    return render(request, 'get_started/index.html')

def login(request):
    return render(request, 'login/index.html')

def signup(request):
    return render(request, 'signup/index.html')

#degisiklik