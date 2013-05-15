# coding: utf-8
from core import db
import json
from django.http import HttpResponse
from ganymede import settings
from testing_runtime.models import Job, Task
import os
from sqlalchemy import and_
import urllib, httplib

def test_notification( request ) :
    params = { "payload" : json.dumps( {
        "pusher": {
            "name": "skliarpawlo",
            "email": "skliarpawlo@rambler.ru"
        },
        "repository": {
            "fork": False,
            "has_wiki": True,
            "name": "callisto",
            "has_downloads": True,
            "url": "https://github.com/skliarpawlo/test",
            "master_branch": "master",
            "created_at": 1365081327,
            "description": "to test github api",
            "private": False,
            "pushed_at": 1365085780,
            "open_issues": 0,
            "watchers": 0,
            "owner": {
                "name": "skliarpawlo",
                "email": "skliarpawlo@rambler.ru"
            },
            "has_issues": True,
            "forks": 0,
            "stargazers": 0,
            "id": 9218547, "size": 108
        },
        "after": "4e1d6516633c4fc14341fb75d797d09b5b4f99fe",
        "created": True,
        "ref": "refs/heads/develop",
        "before": "0000000000000000000000000000000000000000"
    } ) }

    con = httplib.HTTPConnection( "localhost", settings.SERVER_PORT )
    con.request(
        "POST",
        "/github/notify",
        urllib.urlencode(params),
        {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }
    )

    return HttpResponse({"status" : "ok"}, mimetype="application/json")

def push_notification( request ) :
    log_path = os.path.join( settings.HEAP_PATH, "github.log" )
    with open( log_path, "a" ) as f :
        f.write(u"Client IP: {ip}\n".format(ip=request.META["REMOTE_ADDR"]))
        if request.POST.has_key('payload') :
            try :
                json_resp = json.loads( request.POST['payload'] )

                repo = json_resp[ "repository" ][ "name" ]
                branch = "-"
                if json_resp[ "ref" ][ :len( "refs/heads/" ) ] == "refs/heads/" :
                    branch = json_resp[ "ref" ][ len( "refs/heads/" ): ]

                jobs_to_start = db.session.query( Job ).filter(
                    and_(
                        Job.repo == repo,
                        Job.branch == branch,
                        Job.github == 'yes'
                    )
                ).all()

                f.write( u"repo '{0}' branch '{1}'\n".format( repo, branch ) )

                for job in jobs_to_start :
                    f.write( u"job started #{0}\n".format( job.job_id ) )
                    new_task = Task( job_id = job.job_id, status='waiting', whose='github' )
                    db.session.add( new_task )
            except Exception as ex :
                json_resp = { "status" : "exception raised: {0}".format( str( ex ) ) }
        else :
            json_resp = { "status" : "not github knocking here" }

        f.write( u"\n\n" )
        f.write( json.dumps( json_resp ) )
        f.write( u"\n\n______________________\n\n" )

    return HttpResponse(json_resp, mimetype="application/json")

