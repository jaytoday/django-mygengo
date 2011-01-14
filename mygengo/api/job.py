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

import json
from time import time

from . import Api
from ..crypto import sign
from ..exception import MyGengoException

class Job(Api):
    '''Job API library.

    Extends `mygengo.api.Api`. Contains methods for working with a single job.
    '''

    def getJob(self, id=None, fmt=None, params=None):
        '''Retrieve a specific job.

        Request: translate/job/{id} (GET)

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/' + id
        self.response = self.client.get(url, fmt, params)

    def getComments(self, id=None, fmt=None, params=None):
        '''Retrieve the comment thread for a job.

        Request: translate/job/{id}/comments (GET)

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/%s/comments' %  id
        self.response = self.client.get(url, fmt, params)

    def getFeedback(self, id=None, fmt=None, params=None):
        '''Retrieve the feedback.

        Request: translate/job/{id}/feedback (GET)

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/%s/feedback' %  id
        self.response = self.client.get(url, fmt, params)

    def getRevisions(self, id=None, fmt=None, params=None):
        '''Get list of revision resources for a job.

        Request: translate/job/{id}/revisions (GET)

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/%s/revisions' %  id
        self.response = self.client.get(url, fmt, params)

    def getRevision(self, id=None, rev_id=None, fmt=None, params=None):
        '''Get specific revision for a job.

        Request: translate/job/{id}/revision/{rev_id}

        - `id`: the id of the job to retrieve
        - `rev_id`: the id of the revision to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        id, fmt, params = self._setParams(id, fmt, params)
        if rev_id is None:
            rev_id = self.config.get('rev_id', must_exist=True)
        url = self.config.get('baseurl', must_exist=True) + \
            'translate/job/%s/revision/%s' % (id, rev_id)
        self.response = self.client.get(url, fmt, params)

    def putPurchase(self, id=None, fmt=None, params=None):
        '''Update a job to translate.

        Request: translate/job/{id} (PUT)

        ACTION:
        "purchase" - deducts credits for this job and puts it on the
        translator queue.  If the job is part of a group, all jobs in
        the group must be purchased before any of the jobs will be
        available for translation.

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        if params is None:
            api_key = self.config.get('api_key', must_exist=True)
            private_key = self.config.get('private_key', must_exist=True)
            data = {'action': 'purchase'}
            params = {'api_key': api_key,
                      'ts': str(int(time())),
                      'data': json.dumps(data, separators=(',', ':')),
                      }
            query_json = json.dumps(params, separators=(',', ':'), sort_keys=True)
            params['api_sig'] = sign(query_json, private_key)
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/' + id
        self.response = self.client.put(url, fmt, params)

    def putRevise(self, id=None, fmt=None, params=None):
        '''Update a job to translate.

        Request: translate/job/{id} (PUT)

        ACTION:
        "revise" - returns this job back to the translator for revisions
        comment (required) the reason to the translator for sending the
        job back for revisions.

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        if params is None or not 'data' in params:
            raise MyGengoException('In method putRevise: "params" must contain a valid comment')
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/' + id
        self.response = self.client.put(url, fmt, params)

    def putApprove(self, id=None, fmt=None, params=None):
        '''Update a job to translate.

        Request: translate/job/{id} (PUT)

        ACTION:
        "approve" - approves job
        other parameters
        rating (required) - 1 (poor) to 5 (fantastic)
        for_translator (optional) - comments for the translator
        for_mygengo (optional) - comments for myGengo staff (private)
        public (optional) - 1 (true) / 0 (false, default); whether myGengo can share this feedback publicly

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        if params is None or not 'data' in params:
            raise MyGengoException('In method putApprove: "params" must contain a valid rating')
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/' + id
        self.response = self.client.put(url, fmt, params)

    def putReject(self, id=None, fmt=None, params=None):
        '''Update a job to translate.

        Request: translate/job/{id} (PUT)

        ACTION:
        "reject" - rejects the translation
        other parameters
        reason (required) - "quality", "incomplete", "other"
        comment (required)
        captcha (required) - the captcha image text. Each job in a "reviewable" state will
        have a captcha_url value, which is a URL to an image.  This
        captcha value is required only if a job is to be rejected.
        follow_up (optional) - "requeue" (default) or "cancel"

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        if params is None or not 'data' in params:
            raise MyGengoException('In method putReject: "params" must contain a valid reason, comment and captcha')
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/' + id
        self.response = self.client.put(url, fmt, params)


    def postJob(self, fmt=None, params=None):
        '''Submit a new job for translation.

        Request: translate/job (POST)

        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        if params is None or not 'data' in params:
            raise MyGengoException('In method postJob: "params" Should contain all the required parameters.')
        if fmt is None:
            fmt = self.config.get('format', must_exists=True)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job'
        self.response = self.client.post(url, fmt, params)


    def postComment(self, id=None, fmt=None, params=None):
        '''Submit a new comment to the job's comment thread.

        Request: translate/job/{id}/comment (POST)

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        if params is None or not 'data' in params:
            raise MyGengoException('In method postComment: "params" must contain a valid "body" parameter as the comment')
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/%s/comment' % id
        self.response = self.client.post(url, fmt, params)

    def deleteJob(self, id=None, fmt=None, params=None):
        '''Cancel the job.

        You can only cancel a job if it has not been started already by a
        translator.

        Request: translate/job/{id} (DELETE)

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/' + id
        self.response = self.client.delete(url, fmt, params)

    def previewJob(self, id=None, fmt=None, params=None):
        '''Renders a JPEG preview of the translated text.

        N.B. - if the request is valid, a raw JPEG stream is returned.

        Request:

        - `id`: the id of the job to retrieve
        - `fmt`: the response format, xml or json
        - `params`: all the necessary request parameters (including api_key
        and api_sig)

        Omitted parameters are taken from the config.
        '''
        id, fmt, params = self._setParams(id, fmt, params)
        url = self.config.get('baseurl', must_exist=True) + 'translate/job/%s/preview' % id
        self.response = self.client.get(url, fmt, params)
