from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_started),
    path('login/', views.login),
    path('signup/', views.signup),
]