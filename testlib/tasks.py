# coding: utf-8

import tests_config
import core.urls
import traceback
import core.lock
import core.path

def run_test(test):
    "запускает PageTest"

    success = True
    try :
        test.setUp()
        test.run()
    except AssertionError as ex :
        print u"Assertion failed: {0}".format(ex.message)
        success = False
    except Exception as s :
        print "ERROR: ", s
        print traceback.format_exc()
        success = False
    finally:
        test.tearDown()

        # save result
        status = ''
        if (success) :
            status = 'ACCEPTED'.format(core.urls.domain)
        else :
            status = 'FAILED'.format(core.urls.domain)

    print status
    return success

def run(test) :
    core.path.ensure(test.testDir())
    pid_file = test.pidFile()
    test_pid = core.lock.is_free(pid_file)
    if (test_pid==0):
        core.lock.capture(pid_file)
        run_test(test)
        core.lock.uncapture(pid_file)

def run_all() :
    for x in tests_config.all_tests:
        run( tests_config.all_tests[ x ] )

if (__name__=="__main__"):
    run_all()