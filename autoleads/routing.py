from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/autoleads-creator/$', consumers.AutoleadsConsumer.as_asgi()),
]