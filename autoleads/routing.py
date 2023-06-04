from django.urls import re_path
from . import consumers  # make sure to create consumers.py in your autoleads app

websocket_urlpatterns = [
    re_path(r'^ws/autoleads-creator/$', consumers.AutoleadsConsumer.as_asgi()),
]