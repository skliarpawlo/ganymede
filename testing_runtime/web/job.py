# coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime.models import Job, Task, StoredTest, User, EnvScript
from core import db
import json
from testing_runtime.web import tests
from django.utils.translation import ugettext as _
from decorators import html
from django.template import RequestContext

def json_to_envs( js, job_id=None ) :
    if js is None :
        return []

    envs_params = json.loads( js )
    envs = []

    for env_dict in envs_params :
        model = EnvScript( **env_dict )
        model.job_id = job_id
        envs.append( model )

    return envs


def json_to_users( js ) :
    if js is None :
        return []

    users_ids = json.loads( js )

    users_collect = []
    for user_id in users_ids :
        users_collect.append(
            db.user_session.query( User ).filter( User.user_id == user_id ).one()
        )
    return users_collect


def fetch_users_info( job = None ) :
    res = []
    users = db.user_session.query( User ).all()
    if not (job is None) :
        checked_users = json_to_users( job.users )
    for x in users :
        checked = False
        if not (job is None) :
            if x in checked_users :
                checked = True

        res.append( {
            "id" : x.user_id,
            "name" : x.username,
            "email" : x.email,
            "checked" : checked
        } )
    return res

def json_to_tests( js ) :
    tests_ids = json.loads( js )

    tests_collect = []
    for test_id in tests_ids :
        tests_collect.append(
            db.session.query( StoredTest ).filter( StoredTest.test_id == test_id ).one()
        )
    return tests_collect

def add_job(request) :
    title = html.title([ _('Add job'), _('Jobs'), 'Ganymede' ])
    request.page = "job.add"

    if request.method == 'POST' :
        name = request.POST[ 'name' ]
        repo = request.POST[ 'repo' ]
        branch = request.POST[ 'branch' ]
        users = request.POST[ 'users' ]
        deploy = request.POST[ 'deploy' ]
        job_tests = json_to_tests(request.POST[ 'tests' ])
        job = Job( name=name, repo=repo, branch=branch, tests=job_tests, users=users, deploy=deploy )

        job.envs = json_to_envs( request.POST[ 'envs' ] )

        db.session.add(job)

        for env in job.envs :
            db.session.add( env )

        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/json")
    else :
        tests_data = tests.gather_tests_info()
        users_data = fetch_users_info()
        return render_to_response( 'job/add/add_job.html', {
            'title' : title,
            'tests' : tests_data,
            'users' : users_data,
            'repos' : [],
            'branches' : ['develop', 't-kz']
        }, context_instance=RequestContext(request) )

def list_jobs(request) :
    title = html.title( [ _('Jobs'), 'Ganymede' ] )

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
    return render_to_response( 'job/list/list.html', {
        'title' : title,
        'jobs' : jobs
    }, context_instance=RequestContext(request) )

def remove_job(request) :
    job_id = request.POST[ 'job_id' ]
    db.session.query(Job).filter(Job.job_id == job_id).delete()

    json_resp = json.dumps( { "status" : "ok" } )
    return HttpResponse(json_resp, mimetype="application/json")

def update_job(request, job_id) :
    title = html.title( [ _('Update job') + " #" + str(job_id), _('Jobs'), 'Ganymede' ] )

    if request.method == 'POST' :
        job = db.session.query(Job).filter( Job.job_id == int(job_id) ).one()
        job.name = request.POST[ 'name' ]
        job.repo = request.POST[ 'repo' ]
        job.branch = request.POST[ 'branch' ]
        job.exec_time = request.POST[ 'exec_time' ] if request.POST[ 'exec_time' ] != "" else None
        job.tests = json_to_tests( request.POST[ 'tests' ] )
        job.users = request.POST[ 'users' ]
        job.deploy = request.POST[ 'deploy' ] if not request.POST[ 'deploy' ] == u'' else None

        for env in job.envs :
            db.session.delete( env )

        db.session.commit()

        new_envs = json_to_envs( request.POST[ 'envs' ], job.job_id )

        for env in new_envs :
            job.envs.append( env )

        try :
            db.session.commit()
            json_resp = json.dumps( { "status" : "ok" } )
        except Exception as e :
            db.session.rollback()
            json_resp = json.dumps( { "status" : "error", "content" : str(e) } )

        return HttpResponse(json_resp, mimetype="application/json")
    else :
        job_model = db.session.query( Job ).filter( Job.job_id == job_id ).one()
        job = {
            "job_id" : job_model.job_id,
            "name" : job_model.name,
            "repo" : job_model.repo,
            "branch" : job_model.branch,
            "envs" : job_model.envs,
            "exec_time" : job_model.exec_time.strftime("%H:%M") if not job_model.exec_time is None else "",
            "tests" : job_model.tests,
            "deploy" : job_model.deploy
        }

        tests_ids = []
        for x in job_model.tests :
            tests_ids.append( x.test_id )

        tests_data = tests.gather_tests_info( tests_ids )
        users_data = fetch_users_info( job_model )

        return render_to_response(
            'job/update/update_job.html', {
            'title' : title,
            'job' : job,
            'users' : users_data,
            'tests' : tests_data,
            'repos' : [],
            'branches' : ['develop', 't-kz']
        }, context_instance=RequestContext(request) )
