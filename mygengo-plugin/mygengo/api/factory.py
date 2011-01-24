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

from .account import Account
from .job import Job
from .jobs import Jobs
from .service import Service
from ..exception import MyGengoException

def factory(client, config, api_key=None, private_key=None):
    '''Return an instance of the specified API library.

    `client`: the name of the clinet to instantiate (job, jobs, account or service)
    `config`: the instance of `mygengo.Config`
    `api_key`: the user api key
    `private_key`: the user private key

    Keys are taken from `config` if omitted.
    '''
    mapping = {'job': Job,
               'jobs': Jobs,
               'account': Account,
               'service': Service,
               }
    if not client in mapping:
        raise MyGengoException('Invalid client: %s, accepted clients are: job, jobs, account and service.' %
                               client)
    return mapping[client](config, api_key, private_key)
