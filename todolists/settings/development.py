from .base import *

from todolists import secrets

DEBUG = True


INSTALLED_APPS += [
	'debug_toolbar',
]


SECRET_KEY = secrets.SECRET_KEY


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*', ]


DATABASES = {
  'default': {
	  'ENGINE': 'django.db.backends.postgresql_psycopg2',
	  'NAME': secrets.DB_NAME,
	  'USER': secrets.DB_USER,
	  'PASSWORD': secrets.DB_PASSWORD,
	  'HOST': secrets.DB_HOST,
	  'PORT': secrets.DB_PORT,
  }
}

MIDDLEWARE += [
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}