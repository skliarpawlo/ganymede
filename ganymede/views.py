from django.shortcuts import render_to_response
import ganymede.settings
from django.http import HttpResponse
from testlib import tests_config

def screenshot(request) :
    try :
        fd = open( ganymede.settings.HEAP_PATH + request.path )
        resp = HttpResponse( mimetype='image/png' )
        resp.write( fd.read() )
        fd.close()
        return resp
    except :
        return HttpResponse( content="file {0} not found".format(ganymede.settings.HEAP_PATH + request.path), mimetype='text/plain' )

def index(request) :
    return render_to_response( 'index.html' )

def system_state(request) :
    return render_to_response( 'index.html' )

def create_job(request) :
    tests = []
    for pagetest in tests_config.all_tests :
        test = {}
        test[ 'id' ] = pagetest
        test[ 'url' ] = tests_config.all_tests[ pagetest ].url
        test[ 'doc' ] = tests_config.all_tests[ pagetest ].__doc__
        test[ 'subtests' ] = []
        for subtest in tests_config.all_tests[ pagetest ].subtests :
            stest = {}
            stest[ 'id' ] = subtest.test_id
            stest[ 'doc' ] = subtest.__doc__
            test[ 'subtests' ].append( stest )
        tests.append( test )
    return render_to_response( 'job/create/create_job.html', { 'tests' : tests, 'branches' : ['develop', 't-kz'] } )

def create_test(request) :
    return render_to_response( 'job/list.html' )

def list_tests(request) :
    return render_to_response( 'job/list.html' )

def list_jobs(request) :
    return render_to_response( 'job/list.html' )

def test(request) :
    test_id = request.GET.get('test_id')
    op_id = request.GET.get('op_id')

    message = "OK"
    err = 0
    if (op_id == 'test'):
        pid_file = tests.utils.pid_file(test_id)

        core.path.ensure(tests.utils.test_dir(test_id))

        test_pid = core.lock.is_free(pid_file)
        if (test_pid==0):
            if (mode.mode == mode.PRODUCTION) :
                pid = os.fork()
                if (pid > 0) :
                    message = "test started"
                else:
                    if (test_id == "__test_all__") :
                        tests.tasks.run_all()
                    else:
                        core.lock.capture(pid_file)
                        tests.tasks.run_test(test_id)
                        core.lock.uncapture(pid_file)
                    sys.exit(0)
            else :
                if (test_id == "__test_all__") :
                    tests.tasks.run_all()
                else:
                    core.lock.capture(pid_file)
                    tests.tasks.run_test(test_id)
                    core.lock.uncapture(pid_file)

        else:
            message = "test is running already. PID:{0}".format(test_pid)

    elif (op_id == 'log'):
        cur_domain = request.GET.get('domain');
        if (cur_domain is None) :
            cur_domain = "lun.ua"

        result = db.session.query(TestResult).filter_by(test_id=test_id, domain=cur_domain).order_by(desc(TestResult.exec_time)).first()
        if (result is None):
            message = 'no log available'
        else:
            message = result.log

    return HttpResponse( json.dumps( {
        'status' : err,
        'message' : message
    } ), mimetype='application/json' )