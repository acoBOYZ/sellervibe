from celery import shared_task
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import subprocess
import psutil
import signal
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess
import redis
from amazon.models import ProductService


BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent
load_dotenv(os.path.join(BASE_DIR, '.environ'))
is_server = bool(os.getenv('IS_SERVER').lower() == 'true')

pid_file_path = os.path.join(APP_DIR, 'source/script_pid.json')
script_path = os.path.join(APP_DIR, 'source/main.py')
logging_path = os.path.join(APP_DIR, 'source/logfile.log')

r = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))

@shared_task
def ecommerce_app_fetch_model_via_redis():
    print('ecommerce app fetch model via redis is scheduled...')
    try:
        data = r.get('ecommerce_data_from_app')
        if data is not None:
            r.delete('ecommerce_data_from_app')
            ProductService.sync_bulk_update_ecommerce(json.loads(data))
        else:
            print('ECOMMERCE:No data found in Redis.')
        
    except redis.RedisError as e:
        print(f'ECOMMERCE:An error occurred while fetching data from Redis: {e}')
    except json.JSONDecodeError as e:
        print(f'ECOMMERCE:An error occurred while decoding JSON data from Redis: {e}')

@shared_task
def ecommerce_app_get_model_via_redis():
    print('ecommerce app set model via redis is scheduled...')
    try:
        data = ProductService.get_search_data_for_ecommerce()
        r.delete('ecommerce_data_from_models')
        r.set('ecommerce_data_from_models', json.dumps(data))
        
    except redis.RedisError as e:
        print(f'ECOMMERCE:An error occurred while fetching data from Redis: {e}')
    except json.JSONDecodeError as e:
        print(f'ECOMMERCE:An error occurred while decoding JSON data from Redis: {e}')


@shared_task
def ecommerce_app():
    venv_python_path = os.path.join(BASE_DIR, '.venv/bin/python') if is_server else 'python3'
    is_script_running = False

    script_info = None

    if os.path.exists(pid_file_path):
        with open(pid_file_path, 'r') as f:
            script_info = json.load(f)
    else:
        script_info = {}

    for process in psutil.process_iter():
        try:
            if 'python' in process.name() and process.pid == script_info.get('pid', None) and process.create_time() == script_info.get('start_time', None):
                is_script_running = True
        except (NoSuchProcess, AccessDenied, ZombieProcess):
            pass

    if not is_script_running:
        with open(logging_path, 'w') as f:
            script_process = subprocess.Popen([venv_python_path, script_path], stdout=f, stderr=subprocess.STDOUT)
        script_info = {'pid': script_process.pid, 'start_time': psutil.Process(script_process.pid).create_time()}
        with open(pid_file_path, 'w') as f:
            json.dump(script_info, f)


@shared_task
def stop_ecommerce_app():
    if os.path.exists(pid_file_path):
        with open(pid_file_path, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
    else:
        for process in process_iter():
            try:
                for cmd in process.cmdline():
                    if script_path in cmd:
                        process.kill()
                        break
            except (NoSuchProcess, AccessDenied, ZombieProcess):
                pass


@shared_task
def restart_ecommerce_app():
    stop_ecommerce_app.delay()
    ecommerce_app.delay()