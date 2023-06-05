from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard),
    path('dashboard/', views.dashboard),
    path('creator/', views.creator),
    path('creator/upload-product-files', views.upload_product_files),
    path('creator/force-restart-to-app', views.force_restart_to_app),
]