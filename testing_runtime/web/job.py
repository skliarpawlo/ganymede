# coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime.models import Job, Task, StoredTest
from core import db
import json
from testing_runtime.web import tests
from django.utils.translation import ugettext as _
from decorators import html

def json_to_tests( js ) :
    tests_ids = json.loads( js )

    tests_collect = []
    for test_id in tests_ids :
        tests_collect.append(
            db.session.query( StoredTest ).filter( StoredTest.test_id == test_id ).one()
        )
    return tests_collect

def create_job(request) :
    title = html.title([ _('Create'), _('Job'), _('Ganymede') ])

    if request.method == 'POST' :
        name = request.POST[ 'name' ]
        env = request.POST[ 'env' ]
        repo = request.POST[ 'repo' ]
        branch = request.POST[ 'branch' ]
        job_tests = json_to_tests(request.POST[ 'tests' ])
        job = Job( name=name, env=env, repo=repo, branch=branch, tests=job_tests )

        db.session.add(job)

        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/json")
    else :
        tests_data = tests.gather_tests_info()
        return render_to_response( 'job/create/create_job.html', { 'title' : title,
                                                                   'tests' : tests_data,
                                                                   'repos' : [],
                                                                   'branches' : ['develop', 't-kz'] } )

def list_jobs(request) :
    title = html.title( [ _('List'), _('Job'), _('Ganymede') ] )

    jobs = []
    for job in db.session.query(Job).all() :
        try :
            last_task = db.session.query(Task).\
             filter(Task.job_id == job.job_id).\
             order_by(Task.add_time.desc()).limit(1).one()
        except :
            last_task = None

        jobs.append( {
            "job_id" : job.job_id,
            "name" : job.name,
            "repo" : job.repo,
            "branch" : job.branch,
            "last_status" :  _( "Not executed" ) if (last_task is None) else last_task.status.capitalize(),
            "last_task_id" : None if (last_task is None) else last_task.task_id
        } )
    return render_to_response( 'job/list/list.html', { 'title' : title,
                                                       'jobs' : jobs } )

def remove_job(request) :
    job_id = request.POST[ 'job_id' ]
    db.session.query(Job).filter(Job.job_id == job_id).delete()

    json_resp = json.dumps( { "status" : "ok" } )
    return HttpResponse(json_resp, mimetype="application/json")

def update_job(request, job_id) :
    title = html.title( [ _('Update'), _('Job'), _('Ganymede') ] )

    if request.method == 'POST' :
        job = db.session.query(Job).filter( Job.job_id == job_id ).one()
        job.name = request.POST[ 'name' ]
        job.env = request.POST[ 'env' ]
        job.repo = request.POST[ 'repo' ]
        job.branch = request.POST[ 'branch' ]
        job.tests = json_to_tests( request.POST[ 'tests' ] )

        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/json")
    else :
        job_model = db.session.query( Job ).filter( Job.job_id == job_id ).one()
        job = { "job_id" : job_model.job_id,
                "name" : job_model.name,
                "repo" : job_model.repo,
                "branch" : job_model.branch,
                "env" : job_model.env,
                "tests" : job_model.tests }

        tests_ids = []
        for x in job_model.tests :
            tests_ids.append( x.test_id )

        tests_data = tests.gather_tests_info( tests_ids )

        return render_to_response(
            'job/update/update_job.html', {
            'title' : title,
            'job' : job,
            'tests' : tests_data,
            'repos' : [],
            'branches' : ['develop', 't-kz']
        } )
