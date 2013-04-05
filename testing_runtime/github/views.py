# coding: utf-8
from core import db
import json
from django.http import HttpResponse
from ganymede import settings
from testing_runtime.models import Job
import os
from sqlalchemy import and_
from testing_runtime.management.commands.dailycron import add_task

def push_notification( request ) :

    f = open( os.path.join( settings.HEAP_PATH, "github.log" ), "a" )

    if request.POST.has_key('payload') :
        json_resp = json.loads( request.POST['payload'] )

        repo = json_resp[ "repository" ][ "name" ]
        branch = "-"
        if json_resp[ "ref" ][ :len( "refs/heads/" ) ] == "refs/heads/" :
            branch = json_resp[ "ref" ][ len( "refs/heads/" ): ]

        jobs_to_start = db.session.query( Job ).filter(
            and_(
                Job.repo == repo,
                Job.branch == branch
            )
        ).all()

        f.write( u"repo '{0}' branch '{1}'".format( repo, branch ) )

        for job in jobs_to_start :
            f.write( u"job started #{0} {1}".format( job.job_id, job.name ) )
            add_task( job.job_id )

    else :
        json_resp = { "status" : "not github knocking here" }


    f.write( u"\n\n" )
    f.write( json.dumps( json_resp ) )
    f.write( u"\n\n______________________\n\n" )
    f.close()

    return HttpResponse(json_resp, mimetype="application/json")

