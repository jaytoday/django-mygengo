#!/usr/bin/python
# -*- coding: utf-8 -*-

# job api example
# translate/job (POST)
# translate/job/{id} (PUT)
# translate/job/{id} (GET)
# translate/job/{id} (DELETE)
# translate/job/{id}/comments (GET)
# translate/job/{id}/comment (POST)
# translate/job/{id}/feedback (GET)
# translate/job/{id}/revisions (GET)
# translate/job/{id}/revision/{rev_id} (GET)
# translate/job/{id}/preview (GET)

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
# create the request parameters
params = {'ts': int(time()),
          'api_key': api_key
          }
query_string = urlencode(sorted(params.items(), key=itemgetter(0)))
params['api_sig'] = mygengo.crypto.sign(query_string, private_key)
# get an instance of a Job Client
job_client = mygengo.api.factory('job', config)
# get job_id from config file
job_id = config.get('job_id', must_exist=True)



###################################################################
# Lazy Loading
# translate/job (POST)
# submit job for translation
###################################################################
job = {
    'type': 'text',
    'slug': 'API Job 1 test',
    'body_src': 'Text to be translated goes here.',
    'lc_src': 'en',
    'lc_tgt': 'ja',
    'tier': 'standard',
    'auto_approve': 'true',
    'custom_data': '1234567日本語',
    }

# pack the job
data = {'job': job}

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

# translate/job (POST)
# Submits a job or group of jobs to translate.
job_client.postJob('json', params)
print job_client.getResponseBody()

raise SystemExit
###################################################################


# translate/job/{id} (GET)
# Retrieve a job
job_client.getJob(job_id, 'json', params)
print job_client.getResponseBody()

# translate/job/{id}/comments (GET)
#  Retrieves the comment thread for a job
job_client.getComments(job_id, 'json', params)
print job_client.getResponseBody()

# translate/job/{id}/feedback (GET)
# Retrieves the feedback
job_client.getFeedback(job_id, 'xml', params)
print job_client.getResponseBody()

# translate/job/{id}/revisions (GET)
# Gets list of revision resources for a job.
job_client.getRevisions(job_id, 'json', params)
print job_client.getResponseBody()

# translate/job/{id}/revision/{rev_id}
# Gets specific revision for a job.
# get rev_id from config file
rev_id = config.get('rev_id', must_exist=True)
job_client.getRevision(job_id, rev_id, 'json', params)
print job_client.getResponseBody()

# translate/job/{id} (PUT)
# Updates a job to translate.
# ACTION:
# purchase
job_client.putPurchase(job_id, 'json')
print job_client.getResponseBody()

# translate/job/{id} (PUT)
# Updates a job to translate.
# ACTION:
# "revise" - returns this job back to the translator for revisions
data = {'action': 'revise',
        'comment': 'Not happy with translation.',
        }
params = {'api_key': api_key,
          'ts': str(int(time())),
          'data': json.dumps(data, separators=(',', ':')),
          }
query_json = json.dumps(params, separators=(',', ':'), sort_keys=True)
params['api_sig'] = mygengo.crypto.sign(query_json, private_key)
job_client.putRevise(job_id, 'json', params)
print job_client.getResponseBody()

# translate/job/{id} (PUT)
# Updates a job to translate.
# ACTION:
# "approve" - approves job
# other parameters
# rating (required) - 1 (poor) to 5 (fantastic)
# for_translator (optional) - comments for the translator
# for_mygengo (optional) - comments for myGengo staff (private)
# public (optional) - 1 (true) / 0 (false, default).  whether myGengo can share this feedback publicly
data = {'action': 'approve',
        'rating': '5',
        }
params = {'api_key': api_key,
          'ts': str(int(time())),
          'data': json.dumps(data, separators=(',', ':')),
          }
query_json = json.dumps(params, separators=(',', ':'), sort_keys=True)
params['api_sig'] = mygengo.crypto.sign(query_json, private_key)
job_client.putApprove(job_id, 'json', params)
print job_client.getResponseBody()

# translate/job/{id} (PUT)
# Updates a job to translate.
# "reject" - rejects the translation
# other parameters
# reason (required) - "quality", "incomplete", "other"
# comment (required)
# captcha (required) - the captcha image text. Each job in a "reviewable" state
# will have a captcha_url value, which is a URL to an image.  This captcha value
# is required only if a job is to be rejected.
# follow_up (optional) - "requeue" (default) or "cancel"
data = {'action': 'reject',
        'comment': 'This translation is not really the best.',
        'reason': 'quality',
        'captcha': 'UXPX',
        'follow_up': 'cancel',
        }
params = {'api_key': api_key,
          'ts': str(int(time())),
          'data': json.dumps(data, separators=(',', ':')),
          }
query_json = json.dumps(params, separators=(',', ':'), sort_keys=True)
params['api_sig'] = mygengo.crypto.sign(query_json, private_key)
job_client.putReject(job_id, 'json', params)
print job_client.getResponseBody()

# translate/job/{id}/comment (POST)
# Submits a new comment to the job's comment thread.
data = {'body': 'This is a comment'}
params = {'api_key': api_key,
          'ts': str(int(time())),
          'data': json.dumps(data, separators=(',', ':')),
          }
query_json = json.dumps(params, separators=(',', ':'), sort_keys=True)
params['api_sig'] = mygengo.crypto.sign(query_json, private_key)
job_client.postComment(job_id, 'json', params)
print job_client.getResponseBody()

# translate/job/{id} (DELETE)
# Cancels the job. You can only cancel a job if it has not been
# started already by a translator.
job_client.deleteJob(job_id, 'json')
print job_client.getResponseBody()

# translate/job/{id}/preview
# Renders a JPEG preview of the translated text
# N.B. - if the request is valid, a raw JPEG stream is returned.
job_client.previewJob(job_id)
print job_client.getResponseBody()
