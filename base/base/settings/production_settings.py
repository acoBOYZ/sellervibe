from base.settings.common_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['sellervibe.co', 'wwww.sellervibe.co']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sellervibe',
        'USER': 'acoboyz',
        'PASSWORD': '??Zenerteknoloji2016*',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')