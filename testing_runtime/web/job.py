from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime.models import Job, Task
from core import db
import json
from testing_runtime.web import tests

def create_job(request) :
    if request.method == 'POST' :
        name = request.POST[ 'name' ]
        env = request.POST[ 'env' ]
        repo = request.POST[ 'repo' ]
        branch = request.POST[ 'branch' ]
        tests_json = request.POST[ 'tests' ]

        job = Job( name=name, env=env, repo=repo, branch=branch, tests=tests_json )

        db.session.add(job)

        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/json")
    else :
        tests_data = tests.gather_tests_info()
        return render_to_response( 'job/create/create_job.html', { 'tests' : tests_data, 'repos' : [], 'branches' : ['develop', 't-kz'] } )

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
        db.session.query(Job).filter( Job.name == job_name ).update( {
            "env" : request.POST[ 'env' ],
            "repo" : request.POST[ 'repo' ],
            "branch" : request.POST[ 'branch' ],
            "tests" : request.POST[ 'tests' ]
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
        tests_data = tests.gather_tests_info( json.loads( job_model.tests ) )
        return render_to_response(
            'job/update/update_job.html', {
            'job' : job,
            'tests' : tests_data,
            'repos' : [],
            'branches' : ['develop', 't-kz']
        } )
