from django.shortcuts import render_to_response
import ganymede.settings
import tests.tests_config
import tests.tasks
import tests.utils
from django.http import HttpResponse
import json
import os
import core.lock
from core import urls
import tests.schedule
from core import db
from tests.models import TestResult
from sqlalchemy import desc
import tests.utils

def screenshot(request) :
    try :
        fd = open( ganymede.settings.HEAP_PATH + request.path )
        resp = HttpResponse( mimetype='image/png' )
        resp.write( fd.read() )
        fd.close()
        return resp
    except :
        return HttpResponse( content="file {0} not found".format(ganymede.settings.HEAP_PATH + request.path), mimetype='text/plain' )

def home(request) :
    domains = [ 'develop.lun.ua', 'pasha.lun.ua' ]
    data = {}
    db.init()

    cur_domain = request.GET.get('domain');
    if (cur_domain is None) :
        cur_domain = "lun.ua"

    for test_id in tests.tests_config.all_tests :

        result = db.session.query(TestResult).filter_by(test_id=test_id, domain=cur_domain).order_by(desc(TestResult.exec_time)).first()

        if (result is None) :
            result = TestResult( test_id = test_id, status = '-', log = '', domain='-' )

        pid_file = tests.utils.pid_file(test_id)

        data[test_id] = {}

        data[test_id]['status'] = core.lock.is_free(pid_file)
        data[test_id]['last_result'] = result.status + "[" + result.domain + "]"
        data[test_id]['last_run'] = result.exec_time
        data[test_id]['doc'] = tests.tests_config.all_tests[test_id].__doc__

        # traverse screenshots
        data[test_id]['screenshots'] = []
        photo_dir = tests.utils.photos_dir(test_id)
        for root, dirs, files in os.walk(photo_dir):
            for f in files:
                data[test_id]['screenshots'].append( os.path.relpath(os.path.join(root, f), ganymede.settings.HEAP_PATH) )

    db.close()
    return render_to_response( 'all_tests.html', { 'tests' : data, 'domains' : domains, 'cur_domain' : cur_domain } )

def test(request) :
    test_id = request.GET.get('test_id')
    op_id = request.GET.get('op_id')
    domain = request.GET.get('domain')

    message = "OK"
    err = 0
    if (op_id == 'test'):
        pid_file = tests.utils.pid_file(test_id)

        core.path.ensure(tests.utils.test_dir(test_id))

        test_pid = core.lock.is_free(pid_file)
        if (test_pid==0):
            pid = os.fork()
            if (pid > 0) :
                message = "test started"
            else:
                urls.domain = domain
                if (test_id == "__test_all__") :
                    tests.tasks.run_all()
                else:
                    core.lock.capture(pid_file)
                    tests.tasks.run_test(test_id)
                    core.lock.uncapture(pid_file)
                sys.exit(0)
        else:
            message = "test is running already. PID:{0}".format(test_pid)

    elif (op_id == 'log'):
        db.init()

        cur_domain = request.GET.get('domain');
        if (cur_domain is None) :
            cur_domain = "lun.ua"

        result = db.session.query(TestResult).filter_by(test_id=test_id, domain=cur_domain).order_by(desc(TestResult.exec_time)).first()
        if (result is None):
            message = 'no log available'
        else:
            message = result.log
        db.close()

    return HttpResponse( json.dumps( {
        'status' : err,
        'message' : message
    } ), mimetype='application/json' )