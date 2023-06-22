import aiohttp
import ssl
import certifi
import pickle
from dhooks import Webhook, Embed
import logging

logging.basicConfig(filename='logfile.log', level=logging.debug, format='%(asctime)s - %(message)s')

class AsyncEmbedHandler:
    def __init__(self):
        self.webhook_url:str
        self.embed:Embed
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.load_verify_locations(certifi.where())

    def set_embed(self, embed) -> bool:
        try:
            if embed:
                self.webhook_url = embed.get('webhook')
                description = f"[{embed.get('description')}]({embed.get('description_url')})" if embed.get('description_url') else f"{embed.get('description')}"
                self.embed = Embed(description=description, color=int(embed.get('color', '0'), 16), timestamp='now')
                return True
        except Exception as e:
            logging.error(f"Error in set_embed: {str(e)}")
            return False
        
    def set_author(self, author):
        if author:
            self.embed.set_author(name=author.get('name', ''), icon_url=author.get('icon_url', ''), url=author.get('url', ''))

    def add_fields(self, fields):
        if fields:
            for field in fields:
                self.embed.add_field(name=field.get('name', ''), value=field.get('value', ''), inline=field.get('inline', False))

    def set_footer(self, footer):
        if footer:
            self.embed.set_footer(text=footer.get('text', ''), icon_url=footer.get('icon_url', ''))

    def set_image(self, image):
        if image:
            self.embed.set_image(image)

    def set_thumbnail(self, thumbnail):
        if thumbnail:
            self.embed.set_thumbnail(thumbnail)
    
    async def set_all_attrs(self, config):
        try:
            status = self.set_embed(config.get('embed'))
            if status:
                self.set_author(config.get('author'))
                self.add_fields(config.get('fields'))
                self.set_footer(config.get('footer'))
                self.set_image(config.get('image'))
                self.set_thumbnail(config.get('thumbnail'))
            return status
        except Exception as e:
            logging.error(f"Error in set_all_attrs: {str(e)}")
            return False

    async def send(self, config):
        try:
            status = await self.set_all_attrs(config)
            if status:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context)) as session:
                    async with Webhook.Async(self.webhook_url, session=session) as hook:
                        await hook.send(embed=self.embed)
            else:
                logging.warning("Warning in webhook config dict!")
        except Exception as e:
            logging.error(f"Error in send: {str(e)}")
            return False

    def save_webhook_url(self):
        with open('webhook_url.pkl', 'wb') as output:
            pickle.dump(self.webhook_url, output, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_webhook_url():
        with open('webhook_url.pkl', 'rb') as input:
            webhook_url = pickle.load(input)
        return webhook_url

    @staticmethod
    async def delete_webhook():
        try:
            webhook_url = AsyncEmbedHandler.load_webhook_url()
            async with aiohttp.ClientSession() as session:
                async with Webhook.Async(webhook_url, session=session) as hook:
                    await hook.delete()
        except Exception as e:
            logging.error(f"Error in delete_webhook: {str(e)}")