#!/usr/bin/python

# service api example
# translate/service/languages (GET)
# translate/service/language_pairs (GET)

from operator import itemgetter
from time import time
from urllib import urlencode

import mygengo
import mygengo.api
import mygengo.crypto

# read the config
config = mygengo.Config('config.ini')
# create the request parameters
params = {'ts': int(time()),
          'api_key': config.get('api_key', must_exist=True)
          }
query_string = urlencode(sorted(params.items(), key=itemgetter(0)))
params['api_sig'] = mygengo.crypto.sign(query_string, config.get('private_key', must_exist=True))
# get an instance of a Service Client
service = mygengo.api.factory('service', config)

# translate/service/languages (GET)
# Returns a list of supported languages and their language codes.
service.getLanguages('json', params)
print service.getResponseBody()

# translate/service/language_pairs (GET)
# Returns supported translation language pairs, tiers, and credit
# prices.
service.getLanguagePair('json', params)
print service.getResponseBody()
