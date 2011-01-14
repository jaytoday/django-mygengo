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

from operator import itemgetter
from time import time
from urllib import urlencode

from ..client import Client
from ..crypto import sign
from ..exception import MyGengoException

class Api(object):
    def __init__(self, config, api_key=None, private_key=None):
        self.config = config
        if not api_key is None:
            self.config.api_key = api_key
        if not private_key is None:
            self.config.private_key = private_key
        self.client = Client(self.config)
        self.response = None

    def __str__(self):
        return str(self.response) if (not self.response is None) else ''

    def setApiKey(self, api_key):
        '''Overwrite or set the API key.'''
        self.config.api_key = api_key

    def setPrivateKey(self, private_key):
        '''Overwrite or set the private key.'''
        self.config.private_key = private_key

    def setResponseFormat(self, fmt):
        '''Overwrite or set the requested response format.

        Valid formats are ``'xml'`` and ``'json'``.
        '''
        fmt = fmt.lower()
        valid = ('xml', 'json')
        if not fmt in valid:
            raise MyGengoException('Invalid response format: %s, accepted formats are: xml or json.' %
                                   fmt)
        self.config.format = fmt

    def setBaseUrl(self, url):
        '''Overwrite or set the API base URL.'''
        # make sure it ends with /
        self.config.baseurl = url.rtrim('/') + '/'

    def getResponseBody(self):
        '''Return the response body.'''
        self.checkResponse()
        return self.response.read()

    def getResponseCode(self):
        '''Return the HTTP response status code.'''
        self.checkResponse()
        return self.response.status

    def getResponseHeader(self, key):
        '''Return the HTTP header value.

        Return the value of the HTTP header `key`.
        '''
        self.checkResponse()
        return self.response.getheader(key)

    def getResponseHeaders(self):
        '''Return the HTTP headers.

        Return a list of (header, value) tuples.
        '''
        self.checkResponse()
        return self.response.getheaders()

    def checkResponse(self):
        '''Raise an exception if the response is empty.'''
        if self.response is None:
            raise MyGengoException('A valid response is not yet available, please make a request first.')

    def _setParams(self, job_id, fmt, params):
        if job_id is None:
            job_id = self.config.get('job_id', must_exist=True)
        fmt, params = self._setParamsNoId(fmt, params)
        return job_id, fmt, params

    def _setParamsNoId(self, fmt, params):
        if fmt is None:
            fmt = self.config.get('format', must_exist=True)
        if params is None:
            params = {'ts': str(int(time())),
                      'api_key': self.config.get('api_key', must_exist=True),
                      }
            query_string = urlencode(sorted(params.items(), key=itemgetter(0)))
            params['api_sig'] = sign(query_string, self.config.get('private_key', must_exist=True))
        return fmt, params
