from base.settings.common_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IS_SERVER = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
