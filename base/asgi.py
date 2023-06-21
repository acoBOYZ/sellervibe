import os
from pathlib import Path
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.environ'))
is_server = bool(os.getenv('IS_SERVER').lower() == 'true')

if is_server:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development_settings')

django.setup()

from autoleads import routing
from .middleware import AllowedHostsOriginValidator

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
    ),
})