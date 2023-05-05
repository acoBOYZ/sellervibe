from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_started),
    path('login/', views.login_page),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_page),
    path('social/', include('social_django.urls', namespace='social')),

    path('social/google/', views.GoogleLoginView.as_view(), name='google-auth'),
    path('social/google/complete/', views.GoogleLoginView.as_view(), name='google-auth-complete'),
]