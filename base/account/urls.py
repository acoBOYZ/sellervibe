from django.urls import path
from . import views
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.get_started),
    path('login/', views.login),
    path('signup/', views.signup),
]

# serve static files with cache control headers
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, view=cache_control(public=True, max_age=settings.STATICFILES_CACHE_CONTROL))