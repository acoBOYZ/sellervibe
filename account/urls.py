from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getStarted),
    path('home/', views.getStarted),
    path('login/', views.loginPage),
    path('signup/', views.signupPage, name='signup'),
    path('logout/', views.logoutPage),
    path('social/', include('social_django.urls', namespace='social')),

    path('social/google/', views.GoogleLoginView.as_view(), name='google-auth'),
    path('social/google/complete/', views.GoogleLoginView.as_view(), name='google-auth-complete'),
]