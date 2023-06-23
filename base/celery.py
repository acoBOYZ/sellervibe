import os
from celery import Celery
from pathlib import Path
from dotenv import load_dotenv
from celery.signals import after_setup_logger

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.environ'))
is_server = bool(os.getenv('IS_SERVER').lower() == 'true')

if is_server:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development_settings')


app = Celery('base')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from .celeryLogger import LoggingTask
LoggingTask.init()


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    print("Setting up loggers...")
    LoggingTask.setup_loggers(logger, *args, **kwargs)