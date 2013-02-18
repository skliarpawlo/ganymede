# coding: utf-8

import tests_config
import traceback
import core.lock
import core.path
import core.db
import core.git
import core.logger
import ganymede.settings
import os
from testing_runtime import models
from sqlalchemy.orm.exc import NoResultFound
import json
from testlib import utils

def run_test(test):
    "запускает PageTest"
    core.path.ensure(test.testDir())

    success = True
    try :
        test.setUp()
        test.run()
    except AssertionError as ex :
        core.logger.write( u"Assertion failed: {0}".format(ex) )
        test.snapshot()
        success = False
    except Exception as s :
        core.logger.write( u"ERROR: {0}".format(s) )
        core.logger.write( traceback.format_exc() )
        test.snapshot()
        success = False
    finally:
        test.tearDown()

        # save result
        status = ''
        if (success) :
            status = u'success'
        else :
            status = u'fail'

        core.logger.write( status )

    return success

def run_task( task ) :
    "Запускает таск. Вернет True если все тесты пройдут"

    core.path.ensure( task.artifactsDir() )
    result = True

    with core.logger.task_log( task ) :
        core.logger.reset()

        job = task.job
        core.git.checkout_and_deploy( job )

        testcase = get_test_case( job );

        for test in testcase :
            core.logger.write( u"Running test '{0}'".format(utils.test_id(test)) )
            result = run_test( test ) and result

    return result

def run_any() :
    pid_dir = os.path.join( ganymede.settings.HEAP_PATH, "cron")
    core.path.ensure( pid_dir )
    pid_file = os.path.join( pid_dir, "cron.pid" )
    pid = core.lock.is_free( pid_file )
    if (pid == 0) :
        core.lock.capture(pid_file)
        try :
            task = core.db.session.query(models.Task).filter(models.Task.status=='waiting').order_by(models.Task.add_time).limit(1).one()
            core.db.execute( "UPDATE gany_tasks SET status='running' WHERE task_id={0}".format( str(task.task_id) ) )
            try :
                result = run_task( task )
            except :
                result = False
                core.logger.write(u"Exception raised: " + traceback.format_exc(), task_id=task.task_id)
            finally :
                task.artifacts = json.dumps( core.logger.get_artifacts(task.task_id) )
                task.log = core.logger.read(task.task_id)
                task.status = u"success" if result else u"fail"
                core.db.session.query(models.Task)\
                .filter(models.Task.task_id == task.task_id)\
                .update( {"status" : task.status, "log" : task.log, "artifacts" : task.artifacts } )
        except NoResultFound :
            pass
        core.lock.uncapture(pid_file)

def get_test_case( job ) :
    selected_tests = json.loads( job.tests )
    tests = []
    all_tests = tests_config.all_tests()
    for i in all_tests :
        if issubclass(all_tests[i], utils.PageTest) and\
           utils.test_id(all_tests[i]) in selected_tests :
            pagetest = all_tests[i]()
            for j in all_tests :
                if issubclass(all_tests[j], utils.SubTest) and\
                   utils.test_id(all_tests[j]) in selected_tests and\
                   all_tests[j].__parent_test__ == i :
                    subtest = all_tests[j]()
                    pagetest.addSubtest(subtest)
            tests.append( pagetest )
    return tests
