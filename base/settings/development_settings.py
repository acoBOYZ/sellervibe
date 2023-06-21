from base.settings.common_settings import *
from celery.schedules import crontab
from datetime import timedelta


DEBUG = True

ALLOWED_HOSTS = ['web', 'localhost', '127.0.0.1']


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sellervibe',
        'USER': 'acoboyz',
        'PASSWORD': 'SVpsql_P@ssw0rd!123**',
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': '5432',
    }
}

CELERY_BROKER_URL = 'amqp://guest@rabbitmq//'

CELERY_BEAT_SCHEDULE = {
    'keepa_app': {
        'task': 'amazon.tasks.keepa_app',
        'schedule': crontab(minute='*/1'),
        'args': ()
    },
    'keepa_app_fetch_model_via_redis': {
        'task': 'amazon.tasks.keepa_app_fetch_model_via_redis',
        'schedule': crontab(minute='*/1'),
        'args': ()
    },
    'exchangerate_request': {
        'task': 'amazon.tasks.exchangerate_request',
        'schedule': crontab(minute=0, hour='*/3'),
        'args': ()
    },

    'ecommerce_app': {
        'task': 'ecommerce.tasks.ecommerce_app',
        'schedule': crontab(minute='*/1'),
        'args': ()
    },
    'ecommerce_app_fetch_model_via_redis': {
        'task': 'ecommerce.tasks.ecommerce_app_fetch_model_via_redis',
        'schedule': crontab(minute='*/1'),
        'args': ()
    },
    'ecommerce_app_get_model_via_redis': {
        'task': 'ecommerce.tasks.ecommerce_app_get_model_via_redis',
        'schedule': crontab(minute='*/1'),
        'args': ()
    },
    
    'discord_app': {
        'task': 'autoleads.tasks.discord_app',
        'schedule': crontab(minute='*/1'),
        'args': ()
    },
    'discord_app_fetch_model_via_redis': {
        'task': 'autoleads.tasks.discord_app_fetch_model_via_redis',
        'schedule': crontab(minute='*/1'),
        'args': ()
    }
}



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }