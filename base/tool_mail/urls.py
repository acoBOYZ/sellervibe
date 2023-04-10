from django.urls import path
from . import views
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('mail/', views.mail)
]

# serve static files with cache control headers
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, view=cache_control(public=True, max_age=settings.STATICFILES_CACHE_CONTROL))
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# else:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, view=cache_control(public=True, max_age=settings.STATICFILES_CACHE_CONTROL))