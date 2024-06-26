import httpx
import aiohttp
import urllib.parse
import asyncio
import ssl
import certifi
from useragent import user_agent_list
from bs4 import BeautifulSoup
import os
import aiofiles
from img import ImageComparator
import re
import logging

user_agent_list_index = 0

class SmartProxy:
    def __init__(self, config, BASE_DIR):
        self.username = None
        self.password = None
        self.proxy = None
        self.limit_per_minutes = None
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.load_verify_locations(certifi.where())

        self.AMAZON_IMAGE_DIR = os.path.join(BASE_DIR, 'media/amazon/images')
        self.WALMART_IMAGE_DIR = os.path.join(BASE_DIR, 'media/walmart/images')

        if config['is_active']:
            self.username = config['username']
            self.password = config['password']
            self.proxy = config['proxy'].format(self.username, self.password)
            self.limit_per_minutes = config['limit_per_minutes']

    async def fetch_product_data(self, search_param, config):
        logging.info('\n\r')
        logging.info(f'search_param: {search_param}')
        global user_agent_list, user_agent_list_index
        headers = {
            'User-Agent': user_agent_list[user_agent_list_index],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'permissions-policy': 'fullscreen=(self "https://walmart.com"), geolocation=*, camera=()'
        }
        user_agent_list_index = (user_agent_list_index + 1) % len(user_agent_list)

        search_key = config.get('search_key', None)
        asin = search_param.get('asin', None)
        if not search_key or not asin:
            logging.error('ERROR: search_key not found in config')
            return None, asin
        search_text = search_param.get(search_key, None)
        params = config.get('params', None)
        if search_text:
            url = config['base'].format(urllib.parse.quote_plus(search_text))
            try:
                timeout = httpx.Timeout(10.0, read=20.0)
                async with httpx.AsyncClient(proxies={"http://": self.proxy, "https://": self.proxy}, timeout=timeout) as session:
                    resp = await session.get(url=url, headers=headers, params=params)
                    if resp.status_code == 200:
                        product_data = resp.text
                        return product_data, asin
                    else:
                        logging.info(f'Status Code: {resp.status_code}')
            except Exception as e:
                logging.error(f'Error while fetching data: {e}')
                return None, asin
        else:
            logging.error('ERROR: Search parameter was not found!')

        return None, asin

    async def get_products(self, search_param_list, config):
        search_param_batches = []
        search_param_in_current_batch = []
        limit_exceeded = False

        for search_param in search_param_list:
            if search_param:
                search_param_in_current_batch.append(search_param)
                if len(search_param_in_current_batch) >= self.limit_per_minutes:
                    search_param_batches.append(search_param_in_current_batch)
                    search_param_in_current_batch = []
                    limit_exceeded = True

        if search_param_in_current_batch:
            search_param_batches.append(search_param_in_current_batch)

        img_comparator = ImageComparator()
        async with httpx.AsyncClient(proxies={"http://": self.proxy, "https://": self.proxy}) as session:
            for search_param_batch in search_param_batches:
                tasks = [self.fetch_product_data(search_param, config) for search_param in search_param_batch]
                for task in asyncio.as_completed(tasks):
                    try:
                        product_data, asin = await task
                        if product_data and asin:
                            # with open(f'{config.get("task", "")}_{asin}.html', 'w') as f:
                            #     f.write(product_data)
                            #     yield product_data
                            soup = BeautifulSoup(product_data, 'html.parser')

                            product_fetch_list = []
                            pos = 1
                            group_els = soup.select('[role=\"group\"]')

                            for group in group_els:
                                # Extract link-identifier values
                                link_identifiers = [a['link-identifier'] for a in group.find_all('a', {'link-identifier': True})]
                                # Extract all the images
                                images = [img['src'] for img in group.find_all('img', src=True)]
                                for index, image in enumerate(images):
                                    images[index] = self.clean_image_url(image)

                                if len(images) > 0 and len(link_identifiers) > 0:
                                    await self.download_image(images[0], link_identifiers[0])
                                
                                amazon_image = os.path.join(self.AMAZON_IMAGE_DIR, f'{asin}.png')
                                related_image = f'{self.WALMART_IMAGE_DIR}/{link_identifiers[0]}.png'
                                if not await img_comparator.compare(amazon_image, related_image, .84):
                                    break

                                product_fetch_dict = {}
                                product_fetch_dict['updated'] = True
                                product_fetch_dict['asin'] = asin
                                product_fetch_dict['pos'] = pos
                                product_fetch_dict['walmartCode'] = link_identifiers[0]
                                product_fetch_dict['imageUrl'] = images[0]
                                if len(images) > 1:
                                    product_fetch_dict['opportunity'] = True
                                
                                # Extract all the texts
                                texts = [tag.text for tag in group.find_all(text=True) if tag.parent.name != 'script']

                                #Title
                                product_fetch_dict['title'] = texts[0]

                                # Current Price
                                current_price = next((text for text in texts if re.search(r"\$\d+\.\d+(?!\s*/)", text)), None)
                                if not current_price:
                                    current_price = next((text for text in texts if re.search(r"current price \$\d+\.\d+", text)), None)
                                if current_price:
                                    current_price = current_price.replace('current price $', '').replace('Now $', '').replace('$', '')
                                    product_fetch_dict['priceCurrent'] = current_price

                                # Current Price Now
                                current_price_now = next((text for text in texts if re.search(r"Now \$\d+\.\d+(?!\s*/)", text)), None)
                                if not current_price_now:
                                    current_price_now = next((text for text in texts if re.search(r"current price Now \$\d+\.\d+", text)), None)
                                if current_price_now:
                                    current_price_now = current_price_now.replace('current price Now $', '').replace('Now $', '').replace('$', '')
                                    product_fetch_dict['priceCurrent'] = current_price_now

                                priceTemp = product_fetch_dict.get('priceCurrent', '').split('$')
                                if priceTemp and len(priceTemp) > 1 and isinstance(priceTemp, list):
                                    product_fetch_dict['priceCurrent'] = priceTemp[1]
                                    
                                #Current Price Was
                                current_price_was = next((text for text in texts if re.search(r"Was \$\d+\.\d+(?!\s*/)", text)), None)
                                if current_price_was:
                                    current_price_was = current_price_was.replace('Was $', '')
                                    product_fetch_dict['priceWas'] = current_price_was

                                pos += 1
                                product_fetch_list.append(product_fetch_dict)
                                logging.info(f'Found it!: {asin}')

                            yield product_fetch_list
                        else:
                            logging.error(f'ERROR: Product or asin can not found in response {asin}') 
                    except Exception as e:
                        logging.error(f'An error occurred while getting data from html context: {e}')

            if limit_exceeded:
                await asyncio.sleep(60)

    def clean_image_url(self, url):
        formats = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.svg', '.webp', '.ico']
        for format in formats:
            if format in url:
                url = url.split(format, 1)[0] + format
        return url

    async def download_image(self, url, code):
        file_path = f'{self.WALMART_IMAGE_DIR}/{code}.png'
        if os.path.exists(file_path):
            return

        if url.startswith('//'):
            url = 'https:' + url

        if '?' in url:
            url = url.split('?')[0]

        logging.info(f'{code} image will start to download')
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl_context=self.ssl_context)) as session:
                async with session.get(url) as resp:
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    if resp.status == 200:
                        f = await aiofiles.open(file_path, mode='wb')
                        await f.write(await resp.read())
                        await f.close()
        except Exception as e:
            logging.error(f'An error occurred while downloading image: {e}')


