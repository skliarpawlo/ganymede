# coding: utf-8

import tests_config
import traceback
import core.lock
import core.path
import core.db
import core.git
import core.logger
import core.browser
import core.vscreen
import core.mailer
import web.decorators.html
import ganymede.settings
import os
from testing_runtime import models
from sqlalchemy.orm.exc import NoResultFound
import json
from testlib import utils
import sys
import signal
import time

def run_test(test):
    """запускает PageTest"""
    core.path.ensure(test.testDir())

    with core.logger.current_test( test ) :

        success = True
        try :
            test.setUp()
            test.run()
        except AssertionError as ex :
            core.logger.write( u"Assertion failed: {0}".format(ex) )
            test.snapshot()
            success = False
        except utils.SubTestFail as subtestfail :
            core.logger.write( u"Error in subtest: {0}".format(subtestfail) )
            success = False
        except Exception as s :
            core.logger.write( u"Error: {0}".format(s) )
            core.logger.write( traceback.format_exc() )
            test.snapshot()
            success = False
        finally:
            test.tearDown()

            # save result
            if (success) :
                status = u'success'
            else :
                status = u'fail'

            core.logger.set_status( status )
            core.logger.write( web.decorators.html.status_label( status ) )
            core.logger.save_test_result()

    return success

def run_task( task ) :
    """Запускает таск. Вернет True если все тесты пройдут"""

    core.path.ensure( task.artifactsDir() )
    result = True

    with core.logger.current_task( task ) :
        core.logger.reset()

        job = task.job
        core.git.checkout_and_deploy( job )

        testcase = get_test_case( job )

        for test in testcase :
            result = run_test( test ) and result

    return result

def signal_handler( task, start_time ) :
    task_id = task.task_id

    def stop_me( signum, frame ) :
        core.db.reconnect()
        with core.logger.current_task( task_id ) :
            core.logger.write("Task interrupted!", True, True)
            log = core.logger.get_task_log()

        result = json.dumps( core.logger.get_all_results() )
        status = u"fail"
        total_time = time.time() - start_time

        core.db.session.query( models.Task )\
        .filter( models.Task.task_id == task_id )\
        .update( { "status" : status, "result" : result, "log" : log, "total_time" : total_time } )

        pid_dir = os.path.join( ganymede.settings.HEAP_PATH, "cron")
        pid_file = os.path.join( pid_dir, "cron.pid" )
        core.lock.uncapture( pid_file )

        core.browser.stop()
        core.vscreen.stop()
        core.db.close()

        sys.exit()

    signal.signal( signal.SIGUSR1, stop_me )

def run_any() :
    start_time = time.time()
    pid_dir = os.path.join( ganymede.settings.HEAP_PATH, "cron")
    core.path.ensure( pid_dir )
    pid_file = os.path.join( pid_dir, "cron.pid" )
    pid = core.lock.is_free( pid_file )
    if pid == 0 :
        core.lock.capture(pid_file)
        try :
            task = core.db.session.query(models.Task).filter(models.Task.status=='waiting').order_by(models.Task.add_time).limit(1).one()
            task_id = task.task_id
            core.db.execute( "UPDATE gany_tasks SET status='running' WHERE task_id={0}".format( str(task.task_id) ) )
            try :
                signal_handler( task, start_time )
                result = run_task( task )
            except :
                result = False
                with core.logger.current_task( task_id ) :
                    core.logger.write(u"Exception raised: {0}".format(traceback.format_exc().decode('utf-8')))
            finally :
                core.db.reconnect()

                status = u"success" if result else u"fail"

                with core.logger.current_task( task_id ) :
                    res = json.dumps( core.logger.get_all_results() )
                    log = core.logger.get_task_log()

                total_time = time.time() - start_time

                core.db.session.query( models.Task )\
                    .filter( models.Task.task_id == task_id )\
                    .update( { "status" : status, "result" : res, "log" : log, "total_time" : total_time } )

                core.db.session.commit()

                # mail
                if not result :
                    core.mailer.notify( task_id )

        except NoResultFound :
            pass
        core.lock.uncapture( pid_file )

def get_test_case( job ) :
    selected_tests = [ x.test_id for x in job.tests]
    tests = []
    all_tests = tests_config.all_tests()
    for i in all_tests :
        if issubclass(all_tests[i], utils.MainTest) and\
           (i in selected_tests) :
            pagetest = all_tests[i]()
            for j in all_tests :
                if issubclass(all_tests[j], utils.SubTest) and\
                   (j in selected_tests) and\
                   all_tests[j].__parent_test__ == utils.test_name(pagetest) :
                    subtest = all_tests[j]()
                    pagetest.addSubtest(subtest)
            tests.append( pagetest )
    return tests

def stop_current_task() :
    pid_dir = os.path.join( ganymede.settings.HEAP_PATH, "cron")
    core.path.ensure( pid_dir )
    pid_file = os.path.join( pid_dir, "cron.pid" )
    pid = core.lock.is_free( pid_file )
    if not pid == 0 :
        os.kill(pid, signal.SIGUSR1)
