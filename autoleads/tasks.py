from celery import shared_task
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import subprocess
import psutil
import signal
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess
import redis
from base.celeryLogger import LoggingTask

from amazon.models import ProductService


BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent
load_dotenv(os.path.join(BASE_DIR, '.environ'))
is_server = bool(os.getenv('IS_SERVER').lower() == 'true')


pid_file_path = os.path.join(APP_DIR, 'discord/script_pid.json')
script_path = os.path.join(APP_DIR, 'discord/main.py')

r = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))

@shared_task(base=LoggingTask)
def discord_app_fetch_model_via_redis():
    LoggingTask.logger.info('discord app fetch model via redis is scheduled...')
    data = ProductService.get_all_data_for_discord()
    r.delete('discord_data_all')
    r.set('discord_data_all', json.dumps(data))

    data = ProductService.get_walmart_data_for_discord()
    r.delete('discord_data_walmart')
    r.set('discord_data_walmart', json.dumps(data))


@shared_task(base=LoggingTask)
def discord_app():
    LoggingTask.logger.info('discord app is running...')

    venv_python_path = os.path.join(BASE_DIR, '.venv/bin/python') if is_server else 'python3'
    is_script_running = False

    script_info = None

    if os.path.exists(pid_file_path):
        LoggingTask.logger.info(f'{pid_file_path} exist.')
        with open(pid_file_path, 'r') as f:
            script_info = json.load(f)
            LoggingTask.logger.info(f'{pid_file_path}: {script_info}')
    else:
        script_info = {}
        LoggingTask.logger.info(f'{pid_file_path} does not exist.')

    for process in psutil.process_iter():
        try:
            if 'python' in process.name() and process.pid == script_info.get('pid', None) and process.create_time() == script_info.get('start_time', None):
                is_script_running = True
        except (NoSuchProcess, AccessDenied, ZombieProcess):
            pass
    

    LoggingTask.logger.info(f'script is running: {is_script_running}')

    if not is_script_running:
        script_process = subprocess.Popen([venv_python_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        script_info = {'pid': script_process.pid, 'start_time': psutil.Process(script_process.pid).create_time()}
        with open(pid_file_path, 'w') as f:
            json.dump(script_info, f)



@shared_task(base=LoggingTask)
def stop_discord_app():
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


@shared_task(base=LoggingTask)
def restart_discord_app():
    stop_discord_app.delay()
    discord_app.delay()