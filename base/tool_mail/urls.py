from django.urls import path
from . import views
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('mail/', views.mail),
    path('mail/contacts', views.contacts),
    path('mail/templates', views.templates),
    path('mail/signatures', views.signatures),
    path('mail/send', views.send),
    path('upload_file/', views.upload_file),
    path('save_emails/', views.save_emails),
    path('get_email_names/', views.get_email_names, name='get_email_names'),
    path('get_emails/', views.get_emails, name='get_emails'),
    path('upload_attachments/', views.upload_attachments, name='upload_attachments'),
    path('send_bulk_emails/', views.send_bulk_emails, name='send_bulk_emails'),
]

# serve static files with cache control headers
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, view=cache_control(public=True, max_age=settings.STATICFILES_CACHE_CONTROL))
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# else:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, view=cache_control(public=True, max_age=settings.STATICFILES_CACHE_CONTROL))