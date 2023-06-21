from discord import AsyncEmbedHandler
from trigger import TriggerService
import json
from pathlib import Path
import logging
import asyncio
import os
import aiohttp

from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.environ'))
SERVER_PATH = os.getenv('SERVER_PATH')
GET_ALL_PATH = SERVER_PATH + 'amazon/api/get-all-from-discord'

APP_DIR = Path(__file__).resolve().parent
config_file_path = os.path.join(APP_DIR, 'config.json')


async def main():
    while True:
        if os.path.exists(config_file_path):
            config = {}
            with open(config_file_path, 'r') as f:
                config = json.load(f)

            api = AsyncEmbedHandler()
            if api and config:
                bulk_data = []
                print('discord app main loop...')
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(GET_ALL_PATH) as resp:
                            if resp.status == 200:
                                response_data = await resp.json()
                                if response_data.get('success'):
                                    bulk_data = response_data.get('data')
                                else:
                                    logging.error(f"Error posting data: {response_data.get('error')}")
                            else:
                                logging.error(f'Request to API failed with status {resp.status}.')
                    except Exception as e:
                        logging.error(f'An error occurred while making the request: {e}')

                post_list = TriggerService.control_loop(bulk_data, config, 5)

                # for post in post_list:
                #     await api.send(post)

                await asyncio.sleep(60)
            else:
                logging.error(f'An warning occurred: You dont use keepa api!')
                await asyncio.sleep(60)
        else:
            logging.error(f'An error occurred: Can not find asin_and_domain_data.json file!')
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
