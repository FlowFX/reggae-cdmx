from .common import *

ENVIRONMENT = 'production'
DEBUG = False

# Core settings
ALLOWED_HOSTS = ['.reggae-cdmx.com', ]
INTERNAL_IPS: list = []


# Security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# CSRF_USE_SESSIONS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True  # Force HTTPS

# HSTS
# https://docs.djangoproject.com/en/dev/ref/middleware/#http-strict-transport-security
SECURE_HSTS_SECONDS = 3600


# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath('/var/www/static/reggae-cdmx.com/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath('/var/www/media/reggae-cdmx.com/')


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST': get_secret('DB_HOST'),
        'PORT': get_secret('DB_PORT'),
    },
}


# Rollbar Error Tracking https://rollbar.com/flowfx/Reggae-CDMX/
MIDDLEWARE += ['rollbar.contrib.django.middleware.RollbarNotifierMiddleware']

ROLLBAR = {
    'access_token': get_secret('ROLLBAR_ACCESS_TOKEN'),
    'environment': ENVIRONMENT,
    'branch': 'master',
    'root': BASE_DIR,
}
