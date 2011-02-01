from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect,  iri_to_uri
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from time import time
from operator import itemgetter
from time import time
import datetime
from urllib import urlencode
import logging
import settings

try:
    import json
except:
    from django.utils import simplejson as json

import utils 
from user import models
from user.auth import authenticate
from api import get_mygengo_api, get_api_sig

''' Public views '''


def index(request):
    """ landing page w/ navigation """
    context =  { 'sandbox': settings.DEBUG }   
    if 'user' in request.session:
        user = request.session['user']
        context['authuser'] = user
        try:
            apikey = models.APIKey.objects.get(username=user.username)
        except ObjectDoesNotExist:
            apikey = {}
        context['apikey'] = apikey
    return render_to_response('index.html', RequestContext(request, context))


@utils.handle_api_errors
def overview(request):
    """ overview of orders """
    MAX_JOBS = 5
    context =  {}   
    account, account_params =  get_mygengo_api('account', request)
    account.getBalance('json', account_params)
    balance_response = json.loads(account.getResponseBody())
    if 'response' not in balance_response:
        return HttpResponse('myGengo API error. Check that your API keys are correctly set.')
    context['balance'] = balance_response['response']
    account.getStats('json', account_params)
    context['stats'] = json.loads(account.getResponseBody())['response']
    jobs, jobs_params =  get_mygengo_api('jobs', request)  
    jobs.getJobs('json', jobs_params)   
    jobs_items = {'available':[],'reviewable':[], 'approved': [], 'revising': []}
    joblist = json.loads(jobs.getResponseBody())['response']
    for job_item in joblist[:MAX_JOBS]:
        job_obj = utils.get_job(job_item["job_id"], request)
        if not job_obj:
            continue
        jobs_items[job_obj['job']['status']].append(job_obj)
    context['jobs'] = []
    for job_status in ('available','reviewable','approved', 'revising'):
        context['jobs'].append((job_status, jobs_items[job_status]))
    return render_to_response('overview.html', RequestContext(request, context))

@utils.handle_api_errors
def order(request):
    """ order a job """
    if 'body_src' in request.POST:
        return post_order(request)
    context =  { 'default_lc_tgt': 'Japanese' }
    try:
        context['languages'], context['language_pairs'] = utils.get_language_info(request)   
    except ObjectDoesNotExist:
        return HttpResponse('myGengo API error. Check that your API keys are correctly set.')
    return render_to_response('order.html', RequestContext(request, context))

def preview(request, job_id):
    """ get JPEG image for job """
    job, job_params =  get_mygengo_api('job', request)    
    job.previewJob(job_id, 'json', job_params)
    return HttpResponse(job.response.fp.read(), mimetype="image/jpeg")

@authenticate
def login(request):
    """ landing page w/ navigation """
    return HttpResponseRedirect('/')

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return HttpResponseRedirect('/')
    
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
    job, job_params = get_mygengo_api('job', request)      
    job_params = {
        'api_key': job_params['api_key'],
        '_method': 'post',
        'ts': str(int(time())),
        'data': json.dumps(data, separators=(',', ':'))
    }
    query_json = json.dumps(job_params, separators=(',', ':'), sort_keys=True)
    job_params = get_api_sig(job_params, job, query_json)

    # translate/jobs (POST)
    # Submits a job or group of jobs to translate.
    job.postJob('json', job_params)

    return HttpResponseRedirect('/')

@authenticate
def post_settings(request):
    """ save settings """
    context =  {}  
    if request.POST.get('public_key'):
        try:
            apikey = models.APIKey.objects.get(username=request.session['user'].username)
        except ObjectDoesNotExist:
            apikey = models.APIKey(username=request.session['user'].username)
        apikey.public_key = request.POST['public_key']
        apikey.private_key = request.POST['private_key']
        apikey.save()
    
    return HttpResponseRedirect('/')

    
def post_review(request, job_id):
    """ post a review (approval) """
    
    data = {'approve': True, 'rating': int(request.REQUEST['rating'])}
    job, job_params = get_mygengo_api('job', request)      
    job_params = {
        'api_key': job_params['api_key'],
        '_method': 'post',
        'ts': str(int(time())),
        'data': json.dumps(data, separators=(',', ':'))
    }
    query_json = json.dumps(job_params, separators=(',', ':'), sort_keys=True)
    job_params = get_api_sig(job_params, job, query_json)    
    job.putApprove(job_id, 'json', job_params)
    return HttpResponse(job.getResponseBody())

def post_comment(request, job_id):
    """ post comment """
    data = {'body': request.REQUEST['comment']}
    job, job_params = get_mygengo_api('job', request)      
    job_params = {
        'api_key': job_params['api_key'],
        '_method': 'post',
        'ts': str(int(time())),
        'data': json.dumps(data, separators=(',', ':'))
    }
    query_json = json.dumps(job_params, separators=(',', ':'), sort_keys=True)
    job_params = get_api_sig(job_params, job, query_json)    
    job.postComment(job_id, 'json', job_params)    
    return HttpResponse(job.getResponseBody())

        
def service_quote(request):
    """ get quote for service """

    service, service_params = get_mygengo_api('service', request)
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
    service_params = get_api_sig(service_params, service, query_json)        
    service.getQuote('json', service_params)
    response_json = json.loads(service.getResponseBody())
    logging.info(service_params)
    logging.info(response_json)
    if 'err' in response_json:
        return HttpResponse(json.dumps(response_json), mimetype="application/json")
    job_info = response_json['response']['jobs'][0]
    job_info['credits'] = "%.2f" % round(job_info['credits'],2) # round to 2 decimal places 
    return HttpResponse(json.dumps(job_info), mimetype="application/json")


