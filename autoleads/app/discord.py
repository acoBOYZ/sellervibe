import json
import aiohttp
import ssl
import certifi
from dhooks import Webhook, Embed

class AsyncEmbedHandler:
    def __init__(self, json_data):
        self.data = json_data
        if self.data:
            self.webhook_url = self.data.get('webhook')
            self.embed = Embed(description=f"[{self.data.get('description')}]({self.data.get('description_url')})",
                            color=int(self.data.get('color'), 16), 
                            timestamp=self.data.get('timestamp') if self.data.get('timestamp') == 'now' else None)
            
            self.ssl_context = ssl.create_default_context()
            self.ssl_context.load_verify_locations(certifi.where())
        else:
            return None
        
    def set_author(self):
        author = self.data.get('author')
        if author:
            self.embed.set_author(name=author.get('name'), icon_url=author.get('icon_url'))

    def add_fields(self):
        fields = self.data.get('fields')
        if fields:
            for field in fields:
                self.embed.add_field(name=field.get('name'), value=field.get('value'))

    def set_footer(self):
        footer = self.data.get('footer')
        if footer:
            self.embed.set_footer(text=footer.get('text'), icon_url=footer.get('icon_url'))

    def set_image(self):
        image = self.data.get('image_url')
        if image:
            self.embed.set_image(image)

    def set_thumbnail(self):
        thumbnail = self.data.get('thumbnail_url')
        if thumbnail:
            self.embed.set_thumbnail(thumbnail)

    async def send(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context)) as session:
            async with Webhook.Async(self.webhook_url, session=session) as hook:
                await hook.send(embed=self.embed)