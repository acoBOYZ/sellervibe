from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import json
from channels.db import database_sync_to_async
from models import AppService 

class AutoleadsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('OK')
        self.user = self.scope["user"]
        origin_header = self.scope['headers'].get(b'origin')
        expected_origin = "http://localhost:8000"

        if origin_header is not None:
            origin_header = origin_header.decode('utf-8')

        if origin_header != expected_origin:
            await self.close()
            return
        
        if self.user.is_anonymous:
            await self.close()
        elif not self.user.is_autoleads_creator:
            await self.close()
        else:
            await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        
        if action == 'get_all':
            apps = await self.get_all_apps(self.user)
            await self.send(text_data=json.dumps({
                'action': 'get_all',
                'apps': apps,
            }))
        elif action == 'set_all':
            apps = text_data_json.get('apps')
            await self.set_all_apps(self.user, apps)
            await self.send(text_data=json.dumps({
                'action': 'set_all',
                'success': True,
            }))
        else:
            await self.send(text_data=json.dumps({
                'error': 'Invalid action',
            }))

    @database_sync_to_async
    def get_all_apps(self, user):
        return AppService.get_all(user=user)

    @database_sync_to_async
    def set_all_apps(self, user, apps):
        return AppService.set_all(user=user, apps=apps)
