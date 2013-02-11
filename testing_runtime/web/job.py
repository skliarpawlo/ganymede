from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime import tests_config
from testing_runtime.models import Job, Task
from core import db

def _gather_tests_info() :
    tests = []
    for pagetest in tests_config.all_tests :
        test = {}
        test[ 'id' ] = tests_config.all_tests[ pagetest ].id()
        test[ 'url' ] = tests_config.all_tests[ pagetest ].url
        test[ 'doc' ] = tests_config.all_tests[ pagetest ].__doc__
        test[ 'subtests' ] = []
        for subtest in tests_config.all_tests[ pagetest ].subtests :
            stest = {}
            stest[ 'id' ] = subtest.id()
            stest[ 'doc' ] = subtest.__doc__
            test[ 'subtests' ].append( stest )
        tests.append( test )
    return tests

def create_job(request) :
    if request.method == 'POST' :
        import json

        name = request.POST[ 'name' ]
        env = request.POST[ 'env' ]
        repo = request.POST[ 'repo' ]
        branch = request.POST[ 'branch' ]
        tests = request.POST[ 'tests' ]

        job = Job( name=name, env=env, repo=repo, branch=branch, tests=tests )

        db.session.add(job)

        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/x-javascript")
    else :
        tests = _gather_tests_info()
        return render_to_response( 'job/create/create_job.html', { 'tests' : tests, 'repos' : [], 'branches' : ['develop', 't-kz'] } )

def list_jobs(request) :
    import json
    jobs = []
    for job in db.session.query(Job).all() :
        jobs.append( {
            "name" : job.name,
            "repo" : job.repo,
            "branch" : job.branch
        } )
    return render_to_response( 'job/list/list.html', { 'jobs' : jobs } )

def remove_job(request) :
    import json

    job_name = request.POST[ 'job_name' ]
    db.session.query(Job).filter(Job.name == job_name).delete()

    json_resp = json.dumps( { "status" : "ok" } )
    return HttpResponse(json_resp, mimetype="application/x-javascript")

def update_job(request) :
    job_name = request.GET['job_name']
    job_model = db.session.query( Job ).filter( Job.name == job_name ).one()
    job = { "name" : job_model.name,
            "repo" : job_model.repo,
            "branch" : job_model.branch,
            "env" : job_model.env,
            "tests" : job_model.tests }
    tests = _gather_tests_info()
    return render_to_response( 'job/update/update_job.html', { 'job' : job, 'tests' : tests, 'repos' : [], 'branches' : ['develop', 't-kz'] } )
