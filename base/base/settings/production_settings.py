from base.settings.common_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['sellervibe.co', 'www.sellervibe.co', 'en.sellervibe.co', 'tr.sellerbive.co']

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

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

STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static') ]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

SECURE_HSTS_SECONDS = 31536000  # This sets HSTS to 1 year (recommended value)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True