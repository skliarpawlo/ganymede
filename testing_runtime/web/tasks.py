from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime.models import Job, Task
from core import db
import json

def system_state(request) :
    tasks = []
    for task in db.session.query( Task ).order_by( Task.add_time.desc() ) :
        t = {}
        t["id"] = task.task_id
        t["name"] = task.job.name
        t["status"] = task.status
        t["add_time"] = task.add_time
        tasks.append(t)
    return render_to_response('job/state/state.html', {'tasks':tasks})

def run_job( request ) :
    job_name = request.POST['job_name']
    new_task = Task( job_name = job_name, status='WAITING' )
    db.session.add( new_task )
    return HttpResponse( json.dumps( { "status" : "ok" } ), mimetype="application/json" )

def log( request, task_id ) :
    task_model = db.session.query( Task ).filter( Task.task_id == task_id ).one()
    task = {}
    task["id"] = task_model.task_id
    task["name"] = task_model.job.name
    task["branch"] = task_model.job.branch
    task["repo"] = task_model.job.repo
    return render_to_response('job/state/realtime_log.html', {'task':task})
