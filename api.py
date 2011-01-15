#!/usr/bin/python
from operator import itemgetter
from time import time
from urllib import urlencode

import mygengo
import mygengo.api
import mygengo.crypto

DEFAULT_MYGENGO_CONFIG = {
    'baseurl': 'http://api.sandbox.mygengo.com/v1/',
    'api_key': 'l@xVT1_1jHDu-@hDM1|YMv-0ejc]GhSc0J#4BEv(2nO|O6hGBMi0Ba5h0nQQ-N|c',
    'private_key': 'Qs3a9rxfcFXlO-IJk$N2[~KcA($#}-@pOA0^p5FQ7H~8Qxk0FIY{Ks3GzFdSV[0R',
    'format': 'json',
    'debug': 0,
   }

def get_mygengo_api(api_name):
    """ return API client """
    config = mygengo.Config('') # does not work
    for option in DEFAULT_MYGENGO_CONFIG:
        config.set(option, DEFAULT_MYGENGO_CONFIG[option])
    # create the request parameters
    params = {'ts': int(time()),
              'api_key': config.get('api_key', must_exist=True)
              }
    query_string = urlencode(sorted(params.items(), key=itemgetter(0)))
    params['api_sig'] = mygengo.crypto.sign(query_string, config.get('private_key', must_exist=True))
    # get an instance of API Client
    api_client = mygengo.api.factory(api_name, config)
    return api_client, params

def get_api_sig(params, query_json):
    """ get API request signature """
    params['api_sig'] = mygengo.crypto.sign(query_json, DEFAULT_MYGENGO_CONFIG['private_key'])
    return params
