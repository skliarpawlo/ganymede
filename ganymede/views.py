from django.shortcuts import render_to_response
import tests.tests_config
import tests.tasks
import tests.utils
from django.http import HttpResponse
import json
import os
import sys
import core.lock

def home(request) :
    data = {}
    for test_id in tests.tests_config.all_tests :
        pid_file = tests.utils.pid_file(test_id)
        data[test_id] = {}
        data[test_id]['status'] = core.lock.is_free(pid_file)
        data[test_id]['last_result'] = tests.utils.dump_res(test_id)
    return render_to_response( 'all_tests.html', { 'tests' : data } )

def test(request) :
    test_id = request.GET.get('test_id')
    op_id = request.GET.get('op_id')

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