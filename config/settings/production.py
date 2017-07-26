from .common import *


# Core settings
ALLOWED_HOSTS = ['.reggae-cdmx.com', ]
INTERNAL_IPS: list = []


# Security
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True  # Force HTTPS


# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath('/var/www/static/reggae-cdmx.com/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath('/var/www/media/reggae-cdmx.com/')


# # Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST': get_secret('DB_HOST'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Caching
CACHES = {
    'default': {  # Redislabs
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': get_secret('REDIS_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': get_secret('REDIS_PASSWORD'),
        }
    },
}


# Error tracking
#ROLLBAR['environment'] = 'production'