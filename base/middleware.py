import logging
from django.conf import settings
from urllib.parse import urlparse
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

CustomUser = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return None

class AllowedHostsOriginValidator:
    def __init__(self, application):
        self.application = application
        self.logger = logging.getLogger(__name__)

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'origin' in headers:
            origin = headers[b'origin'].decode('utf-8')
            self.logger.debug(f'Origin: {origin}')

            # Ignore the protocol and port
            parsed_origin = urlparse(origin)
            valid = any(
                parsed_origin.hostname == host
                for host in settings.ALLOWED_HOSTS
            )
            if not valid:
                self.logger.warning(f'Invalid origin: {origin}')
                return
        else:
            self.logger.warning('Origin header not found in request')
            return
        return await self.application(scope, receive, send)
