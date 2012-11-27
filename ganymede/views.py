from django.shortcuts import render_to_response
import ganymede.settings
import tests.tests_config
import tests.tasks
import tests.utils
from django.http import HttpResponse
import json
import os
import sys
import core.lock
import time
from core import urls
import tests.schedule

def home(request) :
    domains = [ 'develop.lun.ua', 'pasha.lun.ua' ]
    data = {}
    for test_id in tests.tests_config.all_tests :
        pid_file = tests.utils.pid_file(test_id)
        data[test_id] = {}
        data[test_id]['status'] = core.lock.is_free(pid_file)
        data[test_id]['last_result'] = tests.utils.dump_res(test_id)
        # traverse screenshots
        data[test_id]['screenshots'] = []
        data[test_id]['last_run'] = time.ctime(os.path.getmtime(tests.utils.res_file(test_id)))
        data[test_id]['doc'] = tests.tests_config.all_tests[test_id].__doc__
        photo_dir = tests.utils.photos_dir(test_id)
        for root, dirs, files in os.walk(photo_dir):
            for f in files:
                data[test_id]['screenshots'].append( os.path.join( 'static', os.path.relpath(os.path.join(root, f), ganymede.settings.HEAP_PATH) ) )

    return render_to_response( 'all_tests.html', { 'tests' : data, 'domains' : domains } )

def test(request) :
    test_id = request.GET.get('test_id')
    op_id = request.GET.get('op_id')
    domain = request.GET.get('domain')

    message = "OK"
    err = 0
    if (op_id == 'test'):
        pid_file = tests.utils.pid_file(test_id)
        test_pid = core.lock.is_free(pid_file)
        if (test_pid==0):
            pid = os.fork()
            if (pid > 0) :
                message = "test started"
            else:
                urls.domain = domain
                if (test_id == "__test_all__") :
                    tests.schedule.run_all()
                else:
                    core.lock.capture(pid_file)
                    tests.tasks.run_test(test_id)
                    core.lock.uncapture(pid_file)
                sys.exit(0)
        else:
            message = "test is running already. PID:{0}".format(test_pid)

    elif (op_id == 'log'):
        message = tests.utils.dump_log(test_id)

    return HttpResponse( json.dumps( {
        'status' : err,
        'message' : message
    } ), mimetype='application/json' )