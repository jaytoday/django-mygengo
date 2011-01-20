from django.conf import settings
import os

DEBUG = True # change this to False before deploying to production
MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'djangomygengo',                      # Or path to database file if using sqlite3.
  }
}


settings.configure(DEBUG = DEBUG, TEMPLATE_DEBUG = DEBUG, ROOT_URLCONF = 'urls', TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),), STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), 'static')), 
DATABASES=DATABASES, MEDIA_ROOT=MEDIA_ROOT, 
INSTALLED_APPS = ('user','django.contrib.auth', 'django.contrib.sessions','django.contrib.contenttypes'))
