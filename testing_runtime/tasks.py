# coding: utf-8

import tests_config
import core.urls
import traceback
import core.lock
import core.path
import core.db
import ganymede.settings
import os
from testing_runtime import models
from sqlalchemy.orm.exc import NoResultFound

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

def run_task( task ) :
    import pdb; pdb.set_trace()
    print "testing"

def run_any() :
    pid_dir = os.path.join( ganymede.settings.HEAP_PATH, "cron")
    core.path.ensure( pid_dir )
    pid_file = os.path.join( pid_dir, "cron.pid" )
    pid = core.lock.is_free(pid_file)
    if (pid == 0) :
        core.lock.capture(pid_file)

        try :
            task = core.db.session.query(models.Task).filter(models.Task.status=='WAITING').limit(1).one()
            core.db.session.query(models.Task).filter(models.Task.id == task.id).update( {"status" : "RUNNING"} )

            run_task( task )

            core.db.session.query(models.Task).filter(models.Task.id == task.id).update( {"status" : "FINISHED"} )
        except NoResultFound :
            print "Nothing to test"

        core.lock.uncapture(pid_file)

if (__name__=="__main__"):
    run_all()