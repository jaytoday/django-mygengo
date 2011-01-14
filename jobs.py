#!/usr/bin/python
# -*- coding: utf-8 -*-

# jobs api example
# translate/jobs (POST)
# translate/jobs (GET)
# translate/jobs/{id} (GET)

import json
from operator import itemgetter
from time import time
from urllib import urlencode

import mygengo
import mygengo.api
import mygengo.crypto

# read the config
config = mygengo.Config('config.ini')
# retrieve keys from the config
api_key = config.get('api_key', must_exist=True)
private_key = config.get('private_key', must_exist=True)
# retrieve group_id from config, the group_id is normaly returned
# when groupable jobs are submitted with "as_group = 1"
group_id = config.get('group_id', must_exist=True)
# get an instance of a Jobs Client
jobs = mygengo.api.factory('jobs', config)

# Create groupable jobs for submition
job1 = {
    'type': 'text',
    'slug': 'API Job 1 test',
    'body_src': 'Text to be translated goes here.',
    'lc_src': 'en',
    'lc_tgt': 'ja',
    'tier': 'standard',
    'auto_approve': 'true',
    'custom_data': '1234567日本語',
    }

job2 = {
    'type': 'text',
    'slug': 'API Job 1 test',
    'body_src': 'Text to be translated goes here.',
    'lc_src': 'en',
    'lc_tgt': 'ja',
    'tier': 'standard',
    'auto_approve': 'true',
    'custom_data': '1234567日本語',
    }

# pack the jobs
data = {'jobs': {'job_1': job1, 'job_2': job2},
        'as_group': 1,
        'process': 1,
        }

# create the request parameters
params = {'api_key': api_key,
          '_method': 'post',
          'ts': str(int(time())),
          'data': json.dumps(data, separators=(',', ':')),
          }
# convert them to JSON
query_json = json.dumps(params, separators=(',', ':'), sort_keys=True)
# and sign
params['api_sig'] = mygengo.crypto.sign(query_json, private_key)

# translate/jobs (POST)
# Submits a job or group of jobs to translate.
jobs.postJobs('json', params)
print jobs.getResponseBody()

# translate/jobs (GET)
# Retrieves a list of resources for the most recent jobs filtered
# by the given parameters.
jobs.getJobs('json')
print jobs.getResponseBody()

# translate/jobs/{id} (GET)
# Retrieves the group of jobs that were previously submitted
# together.
jobs.getGroupedJobs(group_id, 'json')
print jobs.getResponseBody()
