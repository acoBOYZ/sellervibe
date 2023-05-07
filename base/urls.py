"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('robots.txt', serve, {'document_root': settings.STATIC_ROOT, 'path': 'robots.txt'}),
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('tools/', include('email_tool.urls')),
    path('accounts/profile/', RedirectView.as_view(url='/tools/mail')),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)