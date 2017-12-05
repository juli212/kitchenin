from .base import *

from urllib import parse
import psycopg2


DEBUG = False


SECERT_KEY = os.environ.get('SECRET_KEY')


parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])


conn = psycopg2.connect(
  database=url.path[1:],
  user=url.username,
  password=url.password,
  host=url.hostname,
  port=url.port
)


ALLOWED_HOSTS = ['kitchenin.herokuapp.com','127.0.0.1', ]


DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': os.environ.get('DB_NAME'),
    'USER': os.environ.get('DB_USER'),
    'PASSWORD': os.environ.get('DB_PASSWORD'),
    'HOST': os.environ.get('DB_HOST'),
    'PORT': os.environ.get('DB_PORT'),
  }
}


MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware', ]


import dj_database_url
DATABASES['default'] = dj_database_url.config()

