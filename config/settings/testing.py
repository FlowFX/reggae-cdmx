from .common import *
import sys
import logging

ENVIRONMENT = 'testing'
DEBUG = False

# Use in-memory file storage
DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'

# Speed!
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)


# Fake out migrations to speed up tests
# cf. https://mastodon.social/@webology/99162173318389992
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {}
    }
}

# Disable logging
logging.disable(logging.CRITICAL)

env = get_secret("ENVIRONMENT")

if os.path.isdir('/Volumes/RAMDisk') and not env == 'ci' and 'create-db' not in sys.argv:
    # and this allows you to use --reuse-db to skip re-creating the db,
    # even faster!
    #
    # To create the RAMDisk, use bash:
    # $ hdiutil attach -nomount ram://$((2 * 1024 * SIZE_IN_MB))
    # /dev/disk2
    # $ diskutil eraseVolume HFS+ RAMDisk /dev/disk2
    DATABASES['default']['TEST']['NAME'] = '/Volumes/RAMDisk/reggae-cdmx.test.db.sqlite3'
