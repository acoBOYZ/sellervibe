import logging
from django.conf import settings
from urllib.parse import urlparse
from channels.db import database_sync_to_async

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
