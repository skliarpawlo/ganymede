from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime.models import Job, Task
from core import db
import json
from data import providers
from django.utils.translation import ugettext as _
from decorators import html
import datetime
from django.template import RequestContext

def system_state(request) :
    title = html.title( [ _('System state'), 'Ganymede' ] )

    tasks = []
    for task in providers.tasks( request.GET ) :
        t = {}
        t["id"] = task.task_id
        t["job_name"] = task.job.name
        t["job_id"] = task.job.job_id
        t["status"] = task.status.capitalize()
        t["add_time"] = task.add_time
        if task.total_time < 0 :
            t["total_time"] = "-"
        else :
            t["total_time"] = datetime.timedelta( seconds=task.total_time )
        tasks.append(t)
    if request.is_ajax() :
        return render_to_response(
            'job/state/table.html',
            {'tasks':tasks},
            context_instance=RequestContext(request)
        )
    else :
        return render_to_response(
            'job/state/state.html',
            {'tasks':tasks, 'title':title},
            context_instance=RequestContext(request)
        )

def run_job( request ) :
    job_id = request.POST['job_id']
    new_task = Task( job_id = job_id, status='waiting' )
    db.session.add( new_task )
    return HttpResponse( json.dumps( { "status" : "ok" } ), mimetype="application/json" )

def log( request, task_id ) :
    title = html.title( [ _('Task log') + " #" + str(task_id), _('Tasks'), 'Ganymede' ] )

    task_model = db.session.query( Task ).filter( Task.task_id == task_id ).one()
    task = {}
    task["id"] = task_model.task_id
    task["name"] = task_model.job.name
    task["branch"] = task_model.job.branch
    task["repo"] = task_model.job.repo
    return render_to_response('job/state/realtime_log.html', {'task':task, 'title':title})
