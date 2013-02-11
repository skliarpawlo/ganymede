from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime import tests_config
from testing_runtime.models import Job, Task
from core import db
import json

def system_state(request) :
    tasks = []
    for task in db.session.query( Task ).order_by( Task.add_time ) :
        t = {}
        t["id"] = task.id
        t["name"] = task.job.name
        t["status"] = task.status
        t["add_time"] = task.add_time
        tasks.append(t)
    return render_to_response('job/state/state.html', {'tasks':tasks})

def run_job( request ) :
    import pdb; pdb.set_trace()
    job_name = request.POST['job_name']
    new_task = Task( job_name = job_name, status='WAITING' )
    db.session.add( new_task )
    return HttpResponse( json.dumps( { "status" : "ok" } ), mimetype="application/x-javascript" )

def ajax( request, method ) :
    return HttpResponse( json.dumps( { "method" : method } ), mimetype="application/x-javascript" )
