from smartproxy import SmartProxy
import json
from pathlib import Path
import logging
import asyncio
import os
import redis

from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, '.environ'))

APP_DIR = Path(__file__).resolve().parent
config_file_path = os.path.join(APP_DIR, 'config.json')


async def main():
    r = redis.Redis(host='redis', port=6379, db=0, password='Redis_P@ssw0rd!123**')
    MAX_RETRY_COUNT = 3

    while True:
        config = None
        search_params = None
        api = None
        print('ecommerce app main loop...')
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
            ecommerce_config_list = config.get('ecommerce')
            api = SmartProxy(config.get('smartproxy', None), BASE_DIR)
        if config:
            if api:
                retries = 0
                while retries < MAX_RETRY_COUNT:
                    try:
                        print('retries count:', )
                        data = r.get('ecommerce_data_from_models')
                        if data is not None:
                            search_params = json.loads(data)
                            r.delete('ecommerce_data_from_models')
                            break
                        else:
                            print('ECOMMERCE: No data found in Redis. Retrying in 60 seconds...')
                            retries += 1
                            await asyncio.sleep(10)
                    except redis.RedisError as e:
                        print(f'ECOMMERCE: An error occurred while fetching data from Redis: {e}')
                        retries += 1
                        await asyncio.sleep(10)
                    except json.JSONDecodeError as e:
                        print(f'ECOMMERCE: An error occurred while decoding JSON data from Redis: {e}')
                        retries += 1
                        await asyncio.sleep(10)

                if retries == MAX_RETRY_COUNT:
                    print(f'ECOMMERCE: Unable to fetch data from Redis after {MAX_RETRY_COUNT} attempts. Skipping this cycle.')
                    await asyncio.sleep(10)
                    continue

                if search_params and isinstance(search_params, list):
                    try:
                        bulk_data = []
                        for index, config in enumerate(ecommerce_config_list):
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
                        print(f'An error occurred: {e}')
                        await asyncio.sleep(60)
            else:
                print(f'An warning occurred: You dont use smartproxy api!')
                await asyncio.sleep(60)
        else:
            print(f'An error occurred: Can not find config.json file!')
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
