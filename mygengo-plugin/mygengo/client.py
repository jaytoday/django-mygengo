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

from httplib import HTTPConnection
from urllib import urlencode
from urlparse import urlparse

from .exception import MyGengoException

class Client(object):
    '''HTTP client library'''

    def __init__(self, config):
        self.config = config

    def get(self, url, fmt, params):
        '''Make a HTTP GET request and return the response.

        Make a HTTP GET request to the URL made from a base URL `url` and query
        string parameters `params`. `fmt` denotes a desired response format.
        '''
        return self._httplib_request('GET', url, fmt, params)

    def post(self, url, fmt, params):
        '''Make a HTTP POST request and return the response.

        Make a HTTP POST request to the URL `url`, sending `params` as the body.
        `fmt` denotes a desired response format.
        '''
        return self._httplib_request('POST', url, fmt, params)

    def put(self, url, fmt, params):
        '''Make a HTTP PUT request and return the response.

        Make a HTTP PUT request to the URL `url`, sending `params` as the body.
        `fmt` denotes a desired response format.
        '''
        return self._httplib_request('PUT', url, fmt, params)

    def delete(self, url, fmt, params):
        '''Make a HTTP DELETE request and return the response.

        Make a HTTP DELETE request to the URL made from a base URL `url` and
        query string parameters `params`. `fmt` denotes a desired response
        format.
        '''
        return self._httplib_request('DELETE', url, fmt, params)

    def _httplib_request(self, method, url, fmt, params):
        '''Make a HTTP request via httplib.

        Make a HTTP request to `url` using `method`. `fmt` denotes a desired
        response format (sent as ``Accept:`` header), `params` are sent as
        the query string or the request body, depending on the method.
        Return a `httplib.HTTPResponse` instance.
        '''
        methods = ('DELETE', 'GET', 'POST', 'PUT')
        method = method.upper()
        if not method in methods:
            raise MyGengoException('Invalid or unsupported HTTP method %s' % method)
        query_string = urlencode(params)
        url_parts = urlparse(url)
        path = url_parts.path
        if method in ('POST', 'PUT'):
            body = query_string
        else:
            path += '?' + query_string
            body = None
        if self.config.debug:
            print url_parts.hostname + path
        headers = self._make_header(fmt)
        if method == 'POST':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        try:
            conn = HTTPConnection(url_parts.hostname, url_parts.port)
            headers['User-Agent'] = 'myGengo Django Plugin; Version 1.0; http://www.jamtoday.org/;'
            conn.request(method, path, body, headers=headers)
            return conn.getresponse()
        except Exception, e:
            raise MyGengoException(e.args)

    def _make_header(self, fmt):
        if fmt is None:
            return {}
        fmt = fmt.lower()
        valid = ('xml', 'json')
        if not fmt in valid:
            raise MyGengoException('Invalid response format: %s, accepted formats are: xml or json.' %
                                   fmt)
        return {'Accept': 'application/' + fmt}
