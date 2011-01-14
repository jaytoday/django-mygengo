from django.conf import settings
import os

MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')

settings.configure(DEBUG = True, TEMPLATE_DEBUG = True, ROOT_URLCONF = 'urls', TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),), STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), 'static')), MEDIA_ROOT=MEDIA_ROOT)
