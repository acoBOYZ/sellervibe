from django.urls import path
from . import views


urlpatterns = [
    path('mail/', views.mail)
]