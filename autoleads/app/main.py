import asyncio
import psutil
import os
import sys
import signal
import time
import datetime
from pathlib import Path

from scrap import Scraper
from db import Database
from logger import Logger
from urllib.parse import quote

import json

startTime = datetime.datetime.now()  # Record the start time
proceedTime = 0
isAppRunning = True
APP_DIR = Path(__file__).resolve().parent
runningFile = os.path.join(APP_DIR, 'running.app')
restartFile = os.path.join(APP_DIR, 'restart.app')
runningData = {}
exContentFile = os.path.join(APP_DIR, 'ex.content')

def restartScript():
    python_executable = sys.executable
    os.execv(python_executable, [python_executable, __file__] + sys.argv[1:])

def writeExContent(response):
    global exContentFile
    with open(exContentFile, mode='w', encoding='utf-8') as f:
        content = f.write(response)
    return content

def readExContent():
    global exContentFile
    with open(exContentFile, mode='r', encoding='utf-8') as f:
        content = f.read()
    return content

def write_json_file(filename, data):
    try:
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(data))
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

def read_json_file(filename):
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            content = f.read()
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

async def create_products(db: Database, app_data):
    for product in app_data['amazon_products']:
        existing_product = await db.get_amazon_product(product['ASIN'])
        if existing_product is None:
            await db.insert_amazon_product(product)
        else:
            await db.update_amazon_product(product['ASIN'], {'UPCS': product['UPCS'], 'status': product['status']})

def create_urls(app_data):
    amazon_base_url = app_data['amazon_base_url']
    url_dict = {}
    for product in app_data['amazon_products']:
        asin_url = amazon_base_url + product['ASIN']
        upc_urls = [f"https://www.google.com/search?hl=en&gl=us&q={quote(upc.strip()).replace('%20', '+')}" for upc in product['UPCS'].split(',')]
        url_dict[asin_url] = upc_urls
    return url_dict

async def process_urls_periodically(db: Database, scraper: Scraper, logger: Logger, configFile, selectorFile):
    global startTime, proceedTime, runningFile, isAppRunning
    # exContent = readExContent()
    while True:
        try:
            start_time = time.perf_counter()
            init_cpu_percent = psutil.cpu_percent()
            init_memory = psutil.virtual_memory().used

            appList = read_json_file(configFile)
            loop_time = 1

            if appList:
                selectorConfig = read_json_file(selectorFile)
                app = appList[0]
                loop_time = int(app['loop_time'])

                await create_products(db, app)
                url_dict = create_urls(app)
                app.pop("amazon_products", None)

                # await scraper.scrap_from_amazon(selectorConfig, app, app['amazon_base_url'] + 'B01D58BGTM', exContent)


                # await scraper.process_urls(selectorConfig, app, url_dict)

            final_cpu_percent = psutil.cpu_percent()
            final_memory = psutil.virtual_memory().used

            cpu_percent_diff = final_cpu_percent - init_cpu_percent
            memory_diff = final_memory - init_memory

            cpu_usage = max(0, cpu_percent_diff)
            memory_usage = max(0, memory_diff / (1024 ** 2))

            end_time = time.perf_counter()
            elapsed_time = (end_time - start_time) * 1000

            logger.debug_log(f"Time taken for all urls: {elapsed_time:.2f} ms,\n\r"
                                f"CPU usage: {cpu_usage:.2f}%,\n\r"
                                f"Memory usage: {memory_usage:.2f} MB\n\r")
            
            await asyncio.sleep(loop_time * 60)
        except Exception as e:
            isAppRunning = False
            logger.log_and_write_error('process_urls_periodically', str(e))
            runningData = {"running": False, "proceed_time": proceedTime, "stop_time": str(datetime.datetime.now()), "stop_reason": str(e)}
            write_json_file(runningFile, runningData)
            break


def handle_sigint(signal, frame):
    global proceedTime, runningFile
    runningData = {"running": False, "proceed_time": proceedTime, "stop_time": str(datetime.datetime.now()), "stop_reason": "Stopped from keyboard"}
    write_json_file(runningFile, runningData)
    sys.exit(0)


async def main():
    global startTime, proceedTime, runningFile, restartFile, isAppRunning
    logger = Logger(True, os.path.join(APP_DIR, 'err.log.json'))
    db = Database('scrap.db', logger)
    await db.create_amazon_product_table()
    scraper = Scraper(db=db, logger=logger)
    
    selectorFile = os.path.join(APP_DIR, 'selector.json')
    appFilename = os.path.join(APP_DIR, 'apps.json')
    appList = read_json_file(appFilename)
    # auto_restart = appList[0].get('auto_restart_value', False)

    asyncio.create_task(process_urls_periodically(db, scraper, logger, appFilename, selectorFile))

    while True:
        try:
            if os.path.exists(restartFile):
                logger.debug_log('App forced to restart from creator!')
                os.remove(restartFile)
                restartScript()

            proceedTime = (datetime.datetime.now() - startTime).total_seconds()
            runningData = {"running": True, "proceed_time": proceedTime, "stop_time": "", "stop_reason": ""}
            write_json_file(runningFile, runningData)

            await asyncio.sleep(1)
        except KeyboardInterrupt:
            runningData = {"running": False, "proceed_time": proceedTime, "stop_time": str(datetime.datetime.now()), "stop_reason": ""}
            write_json_file(runningFile, runningData)
            break
        except Exception as e:
            logger.log_and_write_error('main', str(e))
            runningData = {"running": False, "proceed_time": proceedTime, "stop_time": str(datetime.datetime.now()), "stop_reason": str(e)}
            write_json_file(runningFile, runningData)

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, handle_sigint)
        asyncio.run(main())
    except Exception as e:
        runningData = {"running": False, "proceed_time": proceedTime, "stop_time": str(datetime.datetime.now()), "stop_reason": str(e)}
        write_json_file(runningFile, runningData)
    