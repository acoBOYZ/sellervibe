import aiohttp
import time

class SmartProxy:
    BASE_URL = 'https://api.keepa.com/product'

    def __init__(self, config):
        if not config['is_active']:
            return None
        
        self.access_key = config['access_key']
        self.tokens_per_minute = config['tokens_per_minute']
        self.tokens_left = self.tokens_per_minute
        self.single_asin_cost = 3 # calculaate it with all parameters
        self.params = config['params']

    async def fetch_product_data(self, session, asin_list, domain_id):
        params = {
            'key': self.access_key,
            'domain': domain_id,
            'stats': self.params['stats'],
            'buybox': self.params['buybox'],
            'asin': ','.join(asin_list),
            'history': self.params['history']
        }

        try:
            async with session.get(self.BASE_URL, params=params) as resp:
                product_data = await resp.json()
                return product_data
        except Exception as e:
            return None

    async def bulk_fetch_product_data(self, asin_list_batches, domain_id):
        async with aiohttp.ClientSession() as session:
            for asin_list in asin_list_batches:
                yield await self.fetch_product_data(session, asin_list, domain_id)

    async def get_products(self, asin_list, domain_id):
        asin_list_batches = []
        asins_in_current_batch = []
        
        for asin in asin_list:
            asins_in_current_batch.append(asin)
            if len(asins_in_current_batch) * self.single_asin_cost > self.tokens_left:
                asin_list_batches.append(asins_in_current_batch)
                asins_in_current_batch = []

        if asins_in_current_batch:
            asin_list_batches.append(asins_in_current_batch)

        for asin_list in asin_list_batches:
            try:
                force_to_refill = True
                refill_in = 60
                refill_rate = self.tokens_per_minute
                product_data_generator = self.bulk_fetch_product_data([asin_list], domain_id)
                async for product_data in product_data_generator:
                    if product_data:
                        if isinstance(product_data, dict) and ('tokensLeft' in product_data and 'refillIn' in product_data and 'refillRate' in product_data and 'tokensConsumed' in product_data):
                            self.tokens_left = product_data['tokensLeft']
                            refill_in = product_data['refillIn'] / 1000
                            refill_rate = product_data['refillRate']
                            self.single_asin_cost = product_data['tokensConsumed'] // len(product_data['products'])
                            force_to_refill = False
                        yield product_data

                    if (self.tokens_left < len(asin_list) * self.single_asin_cost) or force_to_refill:
                        time.sleep(refill_in)
                        self.tokens_left += refill_rate
            except Exception as e:
                print(f'An error occurred: {e}')
