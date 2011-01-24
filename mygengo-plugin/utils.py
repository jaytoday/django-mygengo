from time import time
from operator import itemgetter
from time import time
import datetime
from urllib import urlencode
import logging
from django.core.exceptions import ObjectDoesNotExist

try:
    import json
except:
    from django.utils import simplejson as json

from api import get_mygengo_api, get_api_sig

def get_job(job_id, request):
    """ get job and comments given a job id """
    # TODO: cache 
    job, job_params =  get_mygengo_api('job', request)
    job_params["pre_mt"] = 0
    job.getJob(job_id, 'json', job_params)
    job_obj = json.loads(job.getResponseBody())['response']
    job_obj['job']['date'] = datetime.datetime.fromtimestamp(job_obj['job']['ctime']).strftime("%b %d %Y")
    # get comments
    job.getComments(job_id, 'json', job_params)
    job_obj['comments'] = json.loads(job.getResponseBody())['response'].get('thread',[])
    for comment in job_obj['comments']:
        comment['date'] = datetime.datetime.fromtimestamp(comment['ctime']).strftime("%I:%M%p, %b %d %Y")    
    languages, language_pairs = get_language_info(request)
    for lang_type in ('src','tgt'):
        for l in languages:
            if l['lc'] == job_obj['job']['lc_' + lang_type]:
                job_obj['job']['language_' + lang_type] = l['language']
    return job_obj


def get_language_info(request):
    """ get available language info """
    service, params = get_mygengo_api('service', request)
    service.getLanguages('json', params)
    language_response = json.loads(service.getResponseBody())
    if 'response' not in language_response:
        raise ObjectDoesNotExist    
    languages = language_response["response"]
    service.getLanguagePair('json', params)
    language_pairs = json.loads(service.getResponseBody())["response"] 
    return languages, language_pairs

