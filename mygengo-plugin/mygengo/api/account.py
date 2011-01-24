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

class Account(Api):
    '''Account API client library.

    Extends `mygengo.api.Api`. Contains methods for working with an account.
    '''

    def getBalance(self, fmt=None, params=None):
        '''Retrieve account balance in credits.

        Request: account/balance (GET)

        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        fmt, params = self._setParamsNoId(fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'account/balance'
        self.response = self.client.get(url, fmt, params)

    def getStats(self, fmt=None, params=None):
        '''Retrieve account stats, such as orders made.

        Request: account/stats (GET)

        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        fmt, params = self._setParamsNoId(fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'account/stats'
        self.response = self.client.get(url, fmt, params)

