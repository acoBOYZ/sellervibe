from keepaApi import KeepaAPI
import json
from pathlib import Path
import logging
import asyncio
import os
import redis
import logging

from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, '.environ'))

APP_DIR = Path(__file__).resolve().parent
config_file_path = os.path.join(APP_DIR, 'config.json')

logging.basicConfig(filename=os.path.join(APP_DIR, 'logfile.log'), level=logging.DEBUG, format='%(asctime)s - %(message)s')

async def handle_product_data(product_data, r):
    if product_data is None:
        return
    bulk_data = []
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

async def main():
    r = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))
    while True:
        logging.info('keepa app main loop...')
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                data = json.load(f)

            asins = data['asins']
            domain_ids = data['domain_ids']
            keepa_api_configs = data['keepa_api']

            api_list = []
            for keepa_api_config in keepa_api_configs:
                api_list.append(KeepaAPI(keepa_api_config, BASE_DIR))
            if api_list:
                try:
                    for domain_id in domain_ids:
                        for api in api_list:
                            product_data_generator = api.get_products(asins, domain_id)
                            async for product_data in product_data_generator:
                                await handle_product_data(product_data, r)
                    await asyncio.sleep(3)
                except Exception as e:
                    logging.error(f'An error occurred: {e}')
                    await asyncio.sleep(60)
            else:
                logging.error(f'An warning occurred: You dont use keepa api!')
                await asyncio.sleep(60)
        else:
            logging.error(f'An error occurred: Can not find config.json file!')
            await asyncio.sleep(60)

if __name__ == '__main__':
    logging.info('### APPLICATION STARTED ###')
    asyncio.run(main())
