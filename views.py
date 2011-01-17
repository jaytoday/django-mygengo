from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, iri_to_uri
from django.template import RequestContext
from time import time
from operator import itemgetter
from time import time
import datetime
from urllib import urlencode
import logging

try:
    import json
except:
    from django.utils import simplejson as json

import utils 
from api import get_mygengo_api, get_api_sig

''' Public views '''

def index(request):
    """ landing page w/ navigation """
    context =  {}   
    return render_to_response('index.html', RequestContext(request, context))

def overview(request):
    """ overview of orders """
    context =  {}   
    account, account_params =  get_mygengo_api('account')
    account.getBalance('json', account_params)
    context['balance'] = json.loads(account.getResponseBody())['response']
    account.getStats('json', account_params)
    context['stats'] = json.loads(account.getResponseBody())['response']
    jobs, jobs_params =  get_mygengo_api('jobs')  
    jobs.getJobs('json', jobs_params)   
    jobs_items = {'available':[],'reviewable':[], 'approved': []}
    joblist = json.loads(jobs.getResponseBody())['response']
    for job_item in joblist:
        job_obj = utils.get_job(job_item["job_id"])
        jobs_items[job_obj['job']['status']].append(job_obj)
    context['jobs'] = []
    for job_status in ('available','reviewable','approved'):
        context['jobs'].append((job_status, jobs_items[job_status]))
    return render_to_response('overview.html', RequestContext(request, context))

def order(request):
    """ order a job """
    if request.method == "POST":
        return post_order(request)
    context =  { 'default_lc_tgt': 'Japanese' }
    context['languages'], context['language_pairs'] = utils.get_language_info()        
    return render_to_response('order.html', RequestContext(request, context))

def preview(request, job_id):
    """ get JPEG image for job """
    job, job_params =  get_mygengo_api('job')    
    job.previewJob(job_id, 'json', job_params)
    return HttpResponse(job.response.fp.read(), mimetype="image/jpeg")


''' POST handlers '''

def post_order(request):
    """ save an order sent in post request """
    
    job_fields = {
        'type': 'text',
        'slug': str(time()),
        'custom_data': str(time()),
        'body_src': request.POST['body_src'],
        'tier': request.POST['tier'], 
        'lc_src': request.POST['lc_src'],
        'lc_tgt': request.POST['lc_tgt'],
    }
    
    for bool_field in ('as_group','auto_approve'):
        if bool_field in request.POST:
            job_fields[bool_field] = 1
        else:
            job_fields[bool_field] = 0
    
    data = {'job':  job_fields }
    job, job_params = get_mygengo_api('job')      
    job_params = {
        'api_key': job_params['api_key'],
        '_method': 'post',
        'ts': str(int(time())),
        'data': json.dumps(data, separators=(',', ':'))
    }
    query_json = json.dumps(job_params, separators=(',', ':'), sort_keys=True)
    job_params = get_api_sig(job_params, query_json)

    # translate/jobs (POST)
    # Submits a job or group of jobs to translate.
    job.postJob('json', job_params)

    return HttpResponseRedirect('/')
    
def post_review(request, job_id):
    """ post a review (approval) """
    
    data = {'approve': True, 'rating': int(request.REQUEST['rating'])}
    job, job_params = get_mygengo_api('job')      
    job_params = {
        'api_key': job_params['api_key'],
        '_method': 'post',
        'ts': str(int(time())),
        'data': json.dumps(data, separators=(',', ':'))
    }
    query_json = json.dumps(job_params, separators=(',', ':'), sort_keys=True)
    job_params = get_api_sig(job_params, query_json)    
    job.putApprove(job_id, 'json', job_params)
    return HttpResponse(job.getResponseBody())

def post_comment(request, job_id):
    """ post comment """
    data = {'body': request.REQUEST['comment']}
    job, job_params = get_mygengo_api('job')      
    job_params = {
        'api_key': job_params['api_key'],
        '_method': 'post',
        'ts': str(int(time())),
        'data': json.dumps(data, separators=(',', ':'))
    }
    query_json = json.dumps(job_params, separators=(',', ':'), sort_keys=True)
    job_params = get_api_sig(job_params, query_json)    
    job.postComment(job_id, 'json', job_params)    
    return HttpResponse(job.getResponseBody())

        
def service_quote(request):
    """ get quote for service """

    service, service_params = get_mygengo_api('service')
    job = {
        'body_src': request.REQUEST['body'],
        'lc_src': request.REQUEST['lc_src'],
        'lc_tgt': request.REQUEST['lc_tgt'],
        'tier': request.REQUEST['tier']
    }
    data = { 'jobs': [job] }
    service_params = {
        'api_key': service_params['api_key'],
        '_method': 'post',
        'ts': str(int(time())),
        'data': json.dumps(data, separators=(',', ':'))
    }
    query_json = json.dumps(service_params, separators=(',', ':'), sort_keys=True)
    service_params = get_api_sig(service_params, query_json)        
    service.getQuote('json', service_params)
    response_json = json.loads(service.getResponseBody())
    if 'err' in response_json:
        return HttpResponse(json.dumps(response_json), mimetype="application/json")
    job_info = response_json['response']['jobs'][0]
    job_info['credits'] = "%.2f" % round(job_info['credits'],2) # round to 2 decimal places 
    return HttpResponse(json.dumps(job_info), mimetype="application/json")


