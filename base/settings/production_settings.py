from base.settings.common_settings import *
from celery.schedules import crontab
from datetime import timedelta


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['161.35.22.147', 'sellervibe.co', 'www.sellervibe.co']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sellervibe',
        'USER': 'acoboyz',
        'PASSWORD': 'SVpsql_P@ssw0rd!123**',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CELERY_BROKER_URL = 'amqp://acoboyz:Rb_MQ@ssw0rd@161.35.22.147//'

CELERY_BEAT_SCHEDULE = {
    'keepa_app': {
        'task': 'amazon.tasks.keepa_app',
        'schedule': crontab(minute='*/3'),
        'args': ()
    },
    'keepa_app_fetch_model_via_redis': {
        'task': 'amazon.tasks.keepa_app_fetch_model_via_redis',
        'schedule': crontab(minute='*/5'),
        'args': ()
    },
    'exchangerate_request': {
        'task': 'amazon.tasks.exchangerate_request',
        'schedule': crontab(minute=0, hour='*/3'),
        'args': ()
    },

    'ecommerce_app': {
        'task': 'ecommerce.tasks.ecommerce_app',
        'schedule': crontab(minute='*/3'),
        'args': ()
    },
    'ecommerce_app_fetch_model_via_redis': {
        'task': 'ecommerce.tasks.ecommerce_app_fetch_model_via_redis',
        'schedule': crontab(minute='*/5'),
        'args': ()
    },
    'ecommerce_app_get_model_via_redis': {
        'task': 'ecommerce.tasks.ecommerce_app_get_model_via_redis',
        'schedule': crontab(minute=0, hour='*/3'),
        'args': ()
    },
    
    'discord_app': {
        'task': 'autoleads.tasks.discord_app',
        'schedule': crontab(minute='*/3'),
        'args': ()
    },
    'discord_app_fetch_model_via_redis': {
        'task': 'autoleads.tasks.discord_app_fetch_model_via_redis',
        'schedule': crontab(minute='*/30'),
        'args': ()
    }
}


SECURE_HSTS_SECONDS = 31536000  # This sets HSTS to 1 year (recommended value)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True