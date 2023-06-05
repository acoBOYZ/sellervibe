from base.settings.common_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
IS_SERVER = False

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




SECURE_HSTS_SECONDS = 31536000  # This sets HSTS to 1 year (recommended value)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True