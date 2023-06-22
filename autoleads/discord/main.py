from discord import AsyncEmbedHandler
from trigger import TriggerService as domainTrigger
from trigger_walmart import TriggerService as walmartTrigger
from post_handler import PostHandler
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
walmart_config_file_path = os.path.join(APP_DIR, 'walmart_config.json')

logging.basicConfig(filename=os.path.join(APP_DIR, 'logfile.log'), level=logging.DEBUG, format='%(asctime)s - %(message)s')

async def main():
    r = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))
    post_handler = PostHandler(host=os.getenv('REDIS_HOST'), port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))
    MAX_RETRY_COUNT = 3

    while True:
        bulk_data = []
        bulk_data_walmart = []
        config = {}
        walmart_config = {}

        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)

        if os.path.exists(walmart_config_file_path):
            with open(walmart_config_file_path, 'r') as f:
                walmart_config = json.load(f)

            api = AsyncEmbedHandler()
            if api:
                logging.info('discord app main loop...')
                retries = 0
                while retries < MAX_RETRY_COUNT:
                    try:
                        data = r.get('discord_data_all')
                        if data is not None:
                            bulk_data = json.loads(data)
                            r.delete('discord_data_all')

                        data = r.get('discord_data_walmart')
                        if data is not None:
                            bulk_data_walmart = json.loads(data)
                            r.delete('discord_data_walmart')

                        if bulk_data or bulk_data_walmart:
                            break
                        else:
                            logging.error('No data found in Redis. Retrying in 60 seconds...')
                            retries += 1
                            await asyncio.sleep(10)
                    except redis.RedisError as e:
                        logging.error(f'An error occurred while fetching data from Redis: {e}')
                        retries += 1
                        await asyncio.sleep(10)
                    except json.JSONDecodeError as e:
                        logging.error(f'An error occurred while decoding JSON data from Redis: {e}')
                        retries += 1
                        await asyncio.sleep(10)

                if retries == MAX_RETRY_COUNT:
                    logging.warning(f'Unable to fetch data from Redis after {MAX_RETRY_COUNT} attempts. Skipping this cycle.')
                    await asyncio.sleep(10)
                    continue

                if bulk_data and config:
                    post_list = []
                    try:
                        post_list = domainTrigger.control_loop(bulk_data, config, 5)
                    except Exception as e:
                        logging.error(f'An error occurred in domainTrigger: {e}')
                    bulk_data.clear()

                    for post in post_list:
                        post = post_handler.check_post(post=post, expiration_time=300)
                        if post:
                            await api.send(post)

                    post_list.clear()  

                bulk_data.clear()

                if bulk_data_walmart and walmart_config:
                    post_list = []
                    try:
                        post_list = walmartTrigger.control_loop(bulk_data_walmart, walmart_config, 5)
                    except Exception as e:
                        logging.error(f'An error occurred in walmartTrigger: {e}')
                    bulk_data.clear()

                    for post in post_list:
                        post = post_handler.check_post(post=post, expiration_time=300)
                        if post:
                            await api.send(post)

                    post_list.clear() 

                await asyncio.sleep(10)
            else:
                logging.warning(f'A warning occurred: You are not using the Discord API!')
                await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
