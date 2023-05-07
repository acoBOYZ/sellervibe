from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getStarted),
    path('home/', views.getStarted, name='get_started'),
    path('login/', views.loginPage, name='login'),
    path('signup/', views.signupPage, name='signup'),
    path('logout/', views.logoutPage, name='logout'),
    path('social/', include('social_django.urls', namespace='social')),

    path('social/google/', views.GoogleLoginView.as_view(), name='google-auth'),
    path('social/google/complete/', views.GoogleLoginView.as_view(), name='google-auth-complete'),
]