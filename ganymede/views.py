import ganymede.settings
from django.shortcuts import render_to_response
import os
from django.http import HttpResponse
import json
import tests.utils
import core

def home(request) :

    test_list = []
    for root, dirs, files in os.walk(ganymede.settings.TESTS_PATH):
        for dir in dirs :
            test_list.append( dir )

    return render_to_response( 'all_tests.html', {
        'tests' : test_list
    } )

def test(request) :
    test_id = request.GET.get('test_id')
    op_id = request.GET.get('op_id')

    message = "OK"
    err = 0
    if (op_id == 'test'):
        stu_pid=core.lock.is_free(tests.utils.pid_file(test_id))
        if (stu_pid==0):
            message = "Test started"
            test = tests.utils.run_test(test_id)
        else :
            message = "Test is running {0}".format(stu_pid)
    elif (op_id == 'log'):
        message = tests.utils.dump_log(test_id)

    return HttpResponse( json.dumps( {
        'status' : err,
        'message' : message
    } ), mimetype='application/json' )

