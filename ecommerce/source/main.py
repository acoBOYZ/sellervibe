from smartproxy import SmartProxy
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
logging.getLogger('asyncio').setLevel(logging.WARNING)


async def main():
    r = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))
    MAX_RETRY_COUNT = 3

    while True:
        config = None
        search_params = None
        api = None
        logging.info('ecommerce app main loop...')
        if os.path.exists(config_file_path):
            logging.info('config exist')
            with open(config_file_path, 'r') as f:
                logging.info('config is reading...')
                config = json.load(f)
                logging.info('config:', config)
            
            ecommerce_config_list = config.get('ecommerce')
            logging.info('ecommerce_config_list:', ecommerce_config_list)
            api = SmartProxy(config.get('smartproxy', None), BASE_DIR)
            logging.info('api:', api)
        if config:
            logging.log('config IN')
            if api:
                logging.log('api IN')
                retries = 0
                while retries < MAX_RETRY_COUNT:
                    try:
                        logging.info('retries count:', retries)
                        data = r.get('ecommerce_data_from_models')
                        if data is not None:
                            search_params = json.loads(data)
                            r.delete('ecommerce_data_from_models')
                            break
                        else:
                            logging.warning('ECOMMERCE: No data found in Redis. Retrying in 10 seconds...')
                            retries += 1
                            await asyncio.sleep(10)
                    except redis.RedisError as e:
                        logging.error(f'ECOMMERCE: An error occurred while fetching data from Redis: {e}')
                        retries += 1
                        await asyncio.sleep(10)
                    except json.JSONDecodeError as e:
                        logging.error(f'ECOMMERCE: An error occurred while decoding JSON data from Redis: {e}')
                        retries += 1
                        await asyncio.sleep(10)

                if retries == MAX_RETRY_COUNT:
                    logging.warning(f'ECOMMERCE: Unable to fetch data from Redis after {MAX_RETRY_COUNT} attempts. Skipping this cycle.')
                    await asyncio.sleep(10)
                    continue

                logging.info('search_params:', search_params)
                if search_params and isinstance(search_params, list):
                    try:
                        for index, config in enumerate(ecommerce_config_list):
                            bulk_data = []
                            product_data_generator = api.get_products(search_params, config)
                            async for product in product_data_generator:
                                if product:
                                    bulk_data.append(product)

                            if bulk_data:
                                old_data = r.get('ecommerce_data_from_app')
                                if old_data is not None:
                                    old_data = json.loads(old_data)
                                else:
                                    old_data = []

                                combined_data = old_data + bulk_data
                                r.set('ecommerce_data_from_app', json.dumps(combined_data))
                                bulk_data.clear()

                    except Exception as e:
                        logging.error(f'An error occurred: {e}')
                        await asyncio.sleep(60)
            else:
                logging.error(f'An warning occurred: You dont use smartproxy api!')
                await asyncio.sleep(60)
        else:
            logging.error(f'An error occurred: Can not find config.json file!')
            await asyncio.sleep(60)

if __name__ == '__main__':
    logging.info('### APPLICATION STARTED ###')
    asyncio.run(main())
