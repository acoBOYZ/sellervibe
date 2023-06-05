from bs4 import BeautifulSoup
import httpx
import asyncio
import re
import time
from urllib.parse import urlencode
from discord import AsyncEmbedHandler

from db import Database
from logger import Logger


from pathlib import Path
import os
import copy

from useragent import user_agent_list
user_agent_list_index = 0

def writeExContent(response):
    with open(os.path.join(Path(__file__).resolve().parent, 'ex.content'), mode='w', encoding='utf-8') as f:
        f.write(response)

class Scraper:
    def __init__(self, db: Database, logger: Logger):
        self.db = db
        self.logger = logger

    def get_proxy_api_url(self, url, proxy, super_proxy):
        if proxy['server_name'] == 'scrapedo':
            payload = {'token': proxy['api_key'], 'url': url, 'geoCode': 'us', 'transparentResponse': True, 'super': super_proxy, 'retryTimeout': '50000', 'customHeaders': True}
            api_url = f'http://api.scrape.do?{urlencode(payload)}'
        elif proxy['server_name'] == 'scraperapi':
            payload = {'api_key': proxy['api_key'], 'url': url}
            api_url = f'http://api.scraperapi.com?{payload}'
        return api_url

    async def fetch(self, client, url, proxy, super_proxy):
        global user_agent_list, user_agent_list_index
        response = None
        headers = {
            'User-Agent': user_agent_list[user_agent_list_index],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'permissions-policy': 'fullscreen=(self "https://example.com"), geolocation=*, camera=()'
        }

        user_agent_list_index = (user_agent_list_index + 1) % len(user_agent_list)

        try:
            url = self.get_proxy_api_url(url, proxy, super_proxy)
            response = await client.get(url=url, headers=headers, timeout=int(proxy['timeout_value']))
            response.raise_for_status()
            if response.status_code == 200:
                return response.text
            else:
                self.logger.log_and_write_error(f'Unexpected status code {response.status_code} for {url}')
                return None
        except httpx.HTTPError as exc:
            pass
            self.logger.log_and_write_error(f'HTTP Exception for {exc.request.url}', exc)

        return None
        
    async def bounded_fetch(self, semaphore, client, asin_url, url, proxy, super_proxy=False):
        async with semaphore:
            try:
                response_text = await self.fetch(client, url, proxy, super_proxy)  # Changed this line
                return (asin_url, url), response_text
            except Exception as e:
                self.logger.log_and_write_error(f'bounded_fetch: {url}', e)
                return (asin_url, url), None

    def has_asin_data(self, asin_code, list_of_asins):
        for asin in list_of_asins:
            if asin['ASIN'] == asin_code and asin['has_ASIN_data']:
                return True
        return False

    def is_asin_status_ok(self, asin_code, list_of_asins):
        for asin in list_of_asins:
            if asin['ASIN'] == asin_code and asin['status']:
                return True
        return False

    async def process_urls(self, selectorConfig, app_config, url_dict):
        proxies = app_config['proxy_settings']
        list_of_asin_has_ASIN_data =  await self.db.get_all_amazon_products_only_if_has_ASIN_data()
        any_asin_has_ASIN_data = any(asin['has_ASIN_data'] for asin in list_of_asin_has_ASIN_data)
        async with httpx.AsyncClient() as client:
            asin_tasks = []
            for asin_url in url_dict.keys():
                asin_code = str(asin_url).replace(app_config['amazon_base_url'], '')
                if self.is_asin_status_ok(asin_code, list_of_asin_has_ASIN_data):
                    for proxy in proxies:
                        semaphore = asyncio.Semaphore(int(proxy['concurrent_requests_limit']))
                        asin_tasks.append(self.bounded_fetch(semaphore, client, asin_url, asin_url, proxy, False))
            
            asin_responses = [await f for f in asyncio.as_completed(asin_tasks)]

            any_asin_successful = any(response_text for (_, _), response_text in asin_responses) or any_asin_has_ASIN_data
            if any_asin_successful:
                other_tasks = []
                asin_code = str(asin_url).replace(app_config['amazon_base_url'], '')
                success = self.has_asin_data(asin_code, list_of_asin_has_ASIN_data)
                for (asin_url, _), response_text in asin_responses:
                    if response_text is not None:
                        success |= await self.scrap_from_amazon(selectorConfig, app_config, asin_url, response_text)
                    if success:
                        for proxy in proxies:
                            semaphore = asyncio.Semaphore(int(proxy['concurrent_requests_limit']))
                            other_tasks.extend([self.bounded_fetch(semaphore, client, asin_url, url, proxy, False) for url in url_dict[asin_url]])
                
                other_responses = [await f for f in asyncio.as_completed(other_tasks)]
                
                for (asin_url, url), response_text in other_responses:
                    if response_text is not None and selectorConfig['google_search']['base_url'] in url:
                        await self.scrap_from_google_search(selectorConfig, app_config, asin_url, url, response_text)
                    else:
                        self.logger.log_and_write_error(f'No response for', url)
    

    async def scrap_from_amazon(self, all_selector, app_config, asin_url, response):
        selector = all_selector['amazon']
        url = asin_url
        asin = str(asin_url).replace(app_config['amazon_base_url'], '')
        data = {}
        soup = BeautifulSoup(response, 'html.parser')

        for key in selector.keys():
            for item in selector.get(key):
                result = ''
                if item['selector'] == 'one':
                    el = soup.select_one(item['select'])
                    if 'all_text' in item:
                        result = el.get_text(separator=item['all_text']).strip()
                    if 'none' in item:
                        result = bool(el == item['none'])
                    elif el:
                        if 'key' in item:
                            result = el[item['key']].strip()
                        else:
                            result = el.text.strip()

                        if 'slice' in item:
                            for slice_text in item['slice']:
                                result = result.replace(slice_text, '').strip()
                else:
                    result = []
                    els = soup.select(item['select'])
                    ignore_after = False
                    if 'for' in item:
                        for el in els:
                            texts = [span.get_text(strip=True).encode("ascii", "ignore").decode() for span in el.select(item['for'])]
                            if 'slice' in item:
                                for slice in item['slice']:
                                    texts = [text.replace(slice, '').strip() for text in texts]
                            if 'ignore_after' in item:
                                for text in texts:
                                    if item['ignore_after'] in text:
                                        ignore_after = True

                            if len(texts) > 0 and not ignore_after:
                                result.append(': '.join(texts))

                data[f'amazon_{key}'] = result
                if result != '' or result != []:
                    break
                

        if data['amazon_price'] != '':
            data['amazon_url'] = url
            data['amazon_asin'] = asin
            self.logger.debug_log(data)        
            await self.db.update_amazon_product(asin, {'ASIN_data': data})
            return True
        
        return False
    
    def check_white_list(self, text, white_list_string):
        white_list = [item.strip() for item in white_list_string.split(',')]
        return any(s in text for s in white_list)
    
    def convert_price_to_float(self, s):
        try:
            if s is not None:
                s = str(s).replace("$", "").replace(' ', '').replace(',', '')
                if s != '':
                    try:
                        float(s)
                    except ValueError:
                        self.logger.log_and_write_error(f"Input {s} is not a number")
                        return 0.0
                    return float(s)
                return 0.0
            return 0.0
        except Exception as e:
            self.logger.log_and_write_error(f"Cannot convert price {s} to float", str(e))
            return 0.0
        
    def replace_webhook_related_values(self, webhook, key_new, value_new):
        key_new = str(key_new)
        value_new = str(value_new)
        for key, value in webhook.items():
            if key == 'webhook' or key == 'timestamp' or key == 'color':
                continue
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, str):
                        value[sub_key] = str(sub_value).replace(key_new, value_new)
            elif isinstance(value, list):
                for i, sub_dict in enumerate(value):
                    if isinstance(sub_dict, dict):
                        for sub_key, sub_value in sub_dict.items():
                            if isinstance(sub_value, str):
                                sub_dict[sub_key] = str(sub_value).replace(key_new, value_new)
            elif isinstance(value, str):
                webhook[key] = str(value).replace(key_new, value_new)
        return webhook

    async def scrap_from_google_search(self, all_selector, app_config, asin_url, url, response):
        selector = all_selector['google_search']
        asin = str(asin_url).replace(app_config['amazon_base_url'], '')
        upc = str(url).replace(selector['base_url'], '')

        soup = BeautifulSoup(response, 'html.parser')
        price_pattern = re.compile(r'\$\d+.\d+')

        containers = soup.select(selector['container'])
        if containers:
            lowest_price = 1000000
            lowest_price_url = ''
            for container in containers:
                if self.check_white_list(container.text, app_config['white_list']):
                    footer = container.select_one(selector['footer'])
                    if footer:
                        prices = price_pattern.findall(footer.text)
                        self.logger.debug_log('asin:', asin, 'prices:', prices)
                        for price in prices:
                            price = self.convert_price_to_float(price)
                            if price < lowest_price:
                                lowest_price = price
                                link = container.select_one(selector['link'])
                                if link:
                                    lowest_price_url = link.get('href')

            if lowest_price_url != '':
                amazon_product = await self.db.get_amazon_product(asin)
                if amazon_product:
                    if isinstance(amazon_product['ASIN_data'], dict):
                        amazon_price = self.convert_price_to_float(amazon_product['ASIN_data']['amazon_price'])
                        product_price = lowest_price
                        self.logger.debug_log(asin, 'amazon_price:', amazon_price, 'product_price:', product_price)

                        if product_price <= (amazon_price * (1 - (self.convert_price_to_float(app_config['compare_value']) / 100.0))):
                            google_product = {
                                'product_price': '$' + str(product_price),
                                'product_url': str(lowest_price_url)
                            }
                            self.logger.debug_log(url, lowest_price_url, f'${product_price}', '\n\r')
                            webhooks_copy = copy.deepcopy(app_config["webhooks"])
                            for webhook in webhooks_copy:
                                config = webhook['config']
                                if config:
                                    for key, value in amazon_product['ASIN_data'].items():
                                        self.replace_webhook_related_values(config, key, value)
                                    for key, value in google_product.items():
                                        self.replace_webhook_related_values(config, key, value)

                            self.logger.debug_log('wehooks:', webhooks_copy)
                            await self.post_webhook(webhooks_copy)
                    else:
                        self.logger.log_and_write_error(f"amazon_product[{asin}] is not a dictionary. It's a ", type(amazon_product['ASIN_data']).__name__)
    
    async def post_webhook(self, webhooks):
        for webhook in webhooks:
            config = webhook['config']
            try:
                handler = AsyncEmbedHandler(config)
                handler.set_author()
                handler.add_fields()
                handler.set_footer()
                handler.set_image()
                handler.set_thumbnail()

                await handler.send()
            except Exception as e:
                self.logger.log_and_write_error(str(webhook['name']), str(e))