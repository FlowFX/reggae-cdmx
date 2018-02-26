from .common import *


# Debug settings
DEBUG = True
ENVIRONMENT = 'development'
INSTALLED_APPS += ['debug_toolbar',]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]
