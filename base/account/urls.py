from django.urls import path, include
from . import views
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.get_started),
    path('login/', views.login_page),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_page),
]

# serve static files with cache control headers
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, view=cache_control(public=True, max_age=settings.STATICFILES_CACHE_CONTROL))