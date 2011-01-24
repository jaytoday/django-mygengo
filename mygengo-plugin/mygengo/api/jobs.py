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

class Jobs(Api):

    '''Jobs API library.

    Extends `mygengo.api.Api`. Contains methods for working with jobs.
    '''

    def postJobs(self, fmt, params):
        '''Submit a job or group of jobs to translate.

        Request: translate/jobs (POST)

        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)
        '''
        url = self.config.get('baseurl', must_exist=True) + 'translate/jobs'
        self.response = self.client.post(url, fmt, params)

    def getJobs(self, fmt=None, params=None):
        '''Retrieve a list of resources for the most recent jobs.

        Retrieve a list of resources for the most recent jobs filtered by
        the given parameters.

        Request: translate/jobs (POST)

        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        fmt, params = self._setParamsNoId(fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/jobs'
        self.response = self.client.get(url, fmt, params)

    def getGroupedJobs(self, id=None, fmt=None, params=None):
        '''Retrieves the group of jobs that were previously submitted together.

        Request: translate/jobs/{id} (GET)

        - `id`: the id of the job group to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/jobs/' + id
        self.response = self.client.get(url, fmt, params)

