from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime import tests_config
from testing_runtime.models import Job, Task
from core import db
import json
import sys
from testlib import utils

def _gather_tests_info( selected_tests = [] ) :
    tests = []

    for i in tests_config.all_tests :
        pagetest = tests_config.all_tests[i]()
        if isinstance(pagetest, utils.PageTest) :
            test = {}
            test[ 'id' ] = utils.test_id(pagetest)
            test[ 'url' ] = pagetest.url
            test[ 'doc' ] = pagetest.__doc__
            test[ 'checked' ] = utils.test_id(pagetest) in selected_tests
            test[ 'subtests' ] = []
            for j in tests_config.all_tests :
                subtest = tests_config.all_tests[j]()
                if isinstance(subtest, utils.SubTest) and \
                   subtest.__parent_test__ == tests_config.all_tests[i] :
                    stest = {}
                    stest[ 'id' ] = utils.test_id(subtest)
                    stest[ 'doc' ] = subtest.__doc__
                    stest[ 'checked' ] = utils.test_id(subtest) in selected_tests
                    test[ 'subtests' ].append( stest )
            tests.append( test )
    return tests

def create_job(request) :
    if request.method == 'POST' :
        name = request.POST[ 'name' ]
        env = request.POST[ 'env' ]
        repo = request.POST[ 'repo' ]
        branch = request.POST[ 'branch' ]
        tests = request.POST[ 'tests' ]

        job = Job( name=name, env=env, repo=repo, branch=branch, tests=tests )

        db.session.add(job)

        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/json")
    else :
        tests = _gather_tests_info()
        return render_to_response( 'job/create/create_job.html', { 'tests' : tests, 'repos' : [], 'branches' : ['develop', 't-kz'] } )

def list_jobs(request) :
    jobs = []
    for job in db.session.query(Job).all() :
        jobs.append( {
            "name" : job.name,
            "repo" : job.repo,
            "branch" : job.branch
        } )
    return render_to_response( 'job/list/list.html', { 'jobs' : jobs } )

def remove_job(request) :
    job_name = request.POST[ 'job_name' ]
    db.session.query(Job).filter(Job.name == job_name).delete()

    json_resp = json.dumps( { "status" : "ok" } )
    return HttpResponse(json_resp, mimetype="application/json")

def update_job(request, job_name) :
    if request.method == 'POST' :
        name = job_name
        env = request.POST[ 'env' ]
        repo = request.POST[ 'repo' ]
        branch = request.POST[ 'branch' ]
        tests = request.POST[ 'tests' ]

        job = db.session.query(Job).filter( Job.name == name ).update( {
            "env" : env,
            "repo" : repo,
            "branch" : branch,
            "tests" : tests
        } )

        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/json")
    else :
        job_name = job_name
        job_model = db.session.query( Job ).filter( Job.name == job_name ).one()
        job = { "name" : job_model.name,
                "repo" : job_model.repo,
                "branch" : job_model.branch,
                "env" : job_model.env,
                "tests" : job_model.tests }
        tests = _gather_tests_info( json.loads( job_model.tests ) )
        return render_to_response(
            'job/update/update_job.html', {
            'job' : job,
            'tests' : tests,
            'repos' : [],
            'branches' : ['develop', 't-kz']
        } )
