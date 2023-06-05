from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
import json
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import AppService,  AuxiliaryService

class AutoleadsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if not self.user:
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
                'action': action,
                'apps': apps,
            }))
        elif action == 'set_all':
            apps = text_data_json.get('apps')
            response = await self.set_all_apps(self.user, apps)
            await self.send(text_data=json.dumps({
                'action': action,
                'response': response,
            }))
        elif action == 'get_info':
            info = await self.get_info_script()
            await self.send(text_data=json.dumps({
                'action': action,
                'info': info,
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

    @sync_to_async
    def get_info_script(self):
        return AuxiliaryService.get_info_script()
