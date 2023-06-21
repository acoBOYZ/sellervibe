from smartproxy import SmartProxy
import json
from pathlib import Path
import logging
import asyncio
import os
import redis

from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.environ'))

APP_DIR = Path(__file__).resolve().parent
asin_and_domain_data_file_path = os.path.join(APP_DIR, 'asin_and_domain_data.json')


async def main():
    r = redis.Redis(host='redis', port=6379, db=0, password='Redis_P@ssw0rd!123**')
    while True:
        print('keepa app main loop...')
        if os.path.exists(asin_and_domain_data_file_path):
            with open(asin_and_domain_data_file_path, 'r') as f:
                data = json.load(f)

            search_params = data['search_params']
            domain_ids = data['domain_ids']
            smartproxy_config = data['smartproxy_config']

            api = SmartProxy(smartproxy_config)
            if api:
                try:
                    bulk_data = []
                    for domain_id in domain_ids:
                        product_data_generator = api.get_products(search_params, domain_id)
                        async for product_data in product_data_generator:

                            for product in product_data.get('products'):
                                product.pop('csv', None)
                                product.pop('buyBoxSellerIdHistory', None)
                                product.pop('variations', None)
                                product.pop('offers', None)
                                product['updated'] = True

                                salesRanks = product.get('salesRanks', None)
                                salesRankReference = product.get('salesRankReference', 0)
                                if salesRankReference > 0:
                                    salesRanksTemp = salesRanks.get(f'{salesRankReference}', None)
                                    if salesRanksTemp and isinstance(salesRanksTemp, list):
                                        product['salesRanks'] = {"rank": salesRanksTemp[-1]}
                                elif salesRanks and isinstance(salesRanks, dict):
                                    product['salesRanks'] = {"rank": next(iter(salesRanks.values()))[-1]}
                                else:
                                    product.pop('salesRanks', None)


                                bulk_data.append(product)

                    if bulk_data:        
                        old_data = r.get('keepa_data_set')
                        if old_data is not None:
                            old_data = json.loads(old_data)
                        else:
                            old_data = []

                        combined_data = old_data + bulk_data
                        r.set('keepa_data_set', json.dumps(combined_data))
                        bulk_data.clear()

                    await asyncio.sleep(3)
                except Exception as e:
                    logging.error(f'An error occurred: {e}')
                    await asyncio.sleep(60)
            else:
                logging.error(f'An warning occurred: You dont use keepa api!')
                await asyncio.sleep(60)
        else:
            logging.error(f'An error occurred: Can not find asin_and_domain_data.json file!')
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
