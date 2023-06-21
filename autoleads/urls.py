from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard),
    path('dashboard/', views.dashboard),
    path('creator/', views.creator),
    path('creator/get-or-set-all-apps', views.get_or_set_all_apps),
    path('creator/upload-product-files', views.upload_product_files),
    # path('creator/force-restart-to-app', views.force_restart_to_app),
    # path('creator/get-info-from-app', views.get_info_from_app),
    # path('creator/force-start-to-app', views.force_start_to_app),
    # path('api/webhook/<str:token>/', views.webhook, name='webhook'),
]