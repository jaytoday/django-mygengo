from django.conf import settings
import os

DEBUG = True # change this to False before deploying to production
TEMPLATE_DEBUG = DEBUG

MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')

STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), 'static'))
INSTALLED_APPS = ('mygengo-plugin','mygengo-plugin.user','django.contrib.auth', 'django.contrib.sessions','django.contrib.contenttypes')

STATICFILES_URL = '/static/'
MEDIA_URL = '/files/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),
                os.path.join(os.path.dirname(__file__), 'mygengo-plugin/templates'))

ROOT_URLCONF = 'urls'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'djangomygengo',                      # Or path to database file if using sqlite3.
  }
}
