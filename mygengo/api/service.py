'''
myGengo API Client

LICENSE

This source file is subject to the new BSD license that came
with this package in the file LICENSE.txt. It is also available 
through the world-wide-web at this URL:
http://mygengo.com/services/api/dev-docs/mygengo-code-license
If you did not receive a copy of the license and are unable to
obtain it through the world-wide-web, please send an email
to contact@mygengo.com so we can send you a copy immediately.

@category   myGengo
@package    API Client Library
@copyright  Copyright (c) 2009-2010 myGengo, Inc. (http://mygengo.com)
@license    http://mygengo.com/services/api/dev-docs/mygengo-code-license   New BSD License
'''

from . import Api

class Service(Api):
    '''Service API library.

    Extends `mygengo.api.Api`.
    '''

    def getLanguages(self, fmt=None, params=None):
        '''Return a list of supported languages and their language codes.

        Request: translate/service/languages (GET)

        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        fmt, params = self._setParamsNoId(fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/service/languages'
        self.response = self.client.get(url, fmt, params)

    def getLanguagePair(self, fmt=None, params=None):
        '''Returns supported translation language pairs, tiers, and credit prices.

        Request: translate/service/language_pairs (GET)

        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        fmt, params = self._setParamsNoId(fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/service/language_pairs'
        self.response = self.client.get(url, fmt, params)

    def getQuote(self, fmt=None, params=None):
        '''Returns quote for body, lc_src, lc_tgt, and tier

        Request: translate/service/quote (POST)

        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        fmt, params = self._setParamsNoId(fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/service/quote'
        self.response = self.client.post(url, fmt, params)
