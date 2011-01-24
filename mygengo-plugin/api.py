#!/usr/bin/python
from operator import itemgetter
from time import time
from urllib import urlencode
from django.core.exceptions import ObjectDoesNotExist
import mygengo
import mygengo.api
import mygengo.crypto
import settings
import logging

from user import models

if settings.DEBUG:
    BASEURL = 'http://api.sandbox.mygengo.com/v1/'
else:
    BASEURL = 'http://api.mygengo.com/v1/'

# these keys will only work on sandbox
SANDBOX_PUBLIC_KEY = 'l@xVT1_1jHDu-@hDM1|YMv-0ejc]GhSc0J#4BEv(2nO|O6hGBMi0Ba5h0nQQ-N|c'
SANDBOX_PRIVATE_KEY = 'Qs3a9rxfcFXlO-IJk$N2[~KcA($#}-@pOA0^p5FQ7H~8Qxk0FIY{Ks3GzFdSV[0R'  
   
DEFAULT_MYGENGO_CONFIG = {
    'baseurl': BASEURL,
    'api_key': SANDBOX_PUBLIC_KEY,
    'private_key': SANDBOX_PRIVATE_KEY,
    'format': 'json',
    'debug': 0,
   }

def get_mygengo_api(api_name, request):
    """ return API client """
    config = mygengo.Config('') # does not work
    for option in DEFAULT_MYGENGO_CONFIG:
        config.set(option, DEFAULT_MYGENGO_CONFIG[option])
    # if user, try getting their saved API info. 
    context =  {}   
    if request.session.get('user'):
        try:
            apikey = models.APIKey.objects.get(
                username=request.session['user'].username)
            config.set('api_key', str(apikey.public_key))
            config.set('private_key', str(apikey.private_key))
        except ObjectDoesNotExist:
            logging.error('apikey not found for user')

    # create the request parameters
    params = {'ts': int(time()),
              'api_key': config.get('api_key', must_exist=True),
              }
    query_string = urlencode(sorted(params.items(), key=itemgetter(0)))
    params['api_sig'] = mygengo.crypto.sign(query_string, config.get('private_key', must_exist=True))
    # get an instance of API Client
    api_client = mygengo.api.factory(api_name, config)
    return api_client, params

def get_api_sig(params, client, query_json):
    """ get API request signature """
    params['api_sig'] = mygengo.crypto.sign(query_json, client.config.private_key)
    return params
