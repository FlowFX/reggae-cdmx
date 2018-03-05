"""Django settings for Reggae CDMX."""
import json
import os

# Never import from Django directly into settings. Except this.
from django.core.exceptions import ImproperlyConfigured
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# JSON-based secrets module (cf. Two Scoops of Django)
try:
    with open(os.path.join(BASE_DIR, 'secrets.json')) as f:
        secrets = json.loads(f.read())
except FileNotFoundError:
    error_msg = 'secrets.json file is missing.'
    raise ImproperlyConfigured(error_msg)


def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        # Return either environment variable or setting from secrets module
        value = os.environ.get(setting)
        if value is None:
            value = secrets[setting]
        return value
    except KeyError:
        error_msg = f'Set the {setting} environment variable!'
        raise ImproperlyConfigured(error_msg)


# Core settings
SECRET_KEY = get_secret('DJANGO_SECRET_KEY'),

ADMINS = [('Florian', 'florian@lexa.mx'),]
ALLOWED_HOSTS: list = []
APPEND_SLASH = True
DEFAULT_CHARSET = 'utf-8'
ENVIRONMENT = 'development'
ROOT_URLCONF = 'config.urls'
SITE_ID = 1
WSGI_APPLICATION = 'config.wsgi.application'

DEBUG = False

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    'django.contrib.admin',
    'django_extensions',
    'anymail',
    'compressor',
    'app.events',
    'app.venues',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Auth and allauth settings
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_PRESERVE_USERNAME_CASING = False
# SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_PROVIDERS = {
#     'facebook': {
#         'METHOD': 'js_sdk',
#     },
# }


# Language and localization
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'app/templates/locale'),
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'


# default CACHE backend
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}


# Email backende
DEFAULT_FROM_EMAIL = "admin@reggae-cdmx.com"
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "MAILGUN_API_KEY": get_secret('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": 'mg.reggae-cdmx.com',
}
SERVER_EMAIL = "django@reggae-cdmx.com"  # for error messages


# Sessions https://docs.djangoproject.com/en/1.11/topics/http/sessions/
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 1209600  # (2 weeks, in seconds)
# SESSION_COOKIE_SECURE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    os.path.abspath(os.path.join(BASE_DIR, 'app/static')),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '.static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '.media'))

INTERNAL_IPS = ['127.0.0.1']
