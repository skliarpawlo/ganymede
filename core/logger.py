from core import memcached
from core import db
from core import path
from testing_runtime import models
import json
import os
import ganymede.settings

_task_id = None
_test = None

####################### ALL
_all = None
def reset() :
    global _all
    _all = []

def save_test_result() :
    global _all
    obj = get_result()
    _all.append( obj )
    memcached.set( derive_task_results_key(), json.dumps( _all ) )

def get_all_results() :
    return json.loads( memcached.get( derive_task_results_key(), "[]" ) )

def derive_task_results_key() :
    _task = get_task()
    if _task == None :
        return "GANY_TASK_RESULT_LOG"
    return "GANY_TASK_RESULT_" + str(_task.task_id)
##########################

def get_task() :
    global _task_id
    return db.session.query( models.Task ).filter( models.Task.task_id == _task_id ).one()

def get_test() :
    global _test
    return _test

def get_result() :
    global _test
    obj = json.loads( memcached.get( derive_test_results_key(), u"{}" ) )
    if not obj.has_key( "artifacts" ) :
        obj["artifacts"] = []
    if not obj.has_key( "log" ) :
        obj["log"] = ""
    if not obj.has_key( "status" ) :
        obj["status"] = "unknown"
    if not obj.has_key( "name" ) :
        obj["name"] = _test.__doc__
    if not obj.has_key( "test_id" ) :
        from testing_runtime import tests_config
        obj["test_id"] = tests_config.test_to_id( _test )
    return obj

def set_result(obj) :
    memcached.set( derive_test_results_key(), json.dumps( obj ) )

# KEYS

def derive_task_log_key() :
    _task = get_task()
    if _task == None :
        return "GANY_TASK_LOG"
    return "GANY_TASK_LOG_" + str(_task.task_id)

def derive_test_results_key() :
    from testing_runtime import tests_config
    _test = get_test()
    _task = get_task()
    if _task == None :
        return "GANY_TEST_RESULT_LOG"
    return "GANY_TEST_RESULT_" + str(_task.task_id) + "_" + str( tests_config.test_to_id( _test ) )

# ARTIFACTS ADDER
def add_artifact( artifact ) :
    _test = get_test()
    _task = get_task()

    heap_len = len(ganymede.settings.HEAP_PATH)
    path.copy( artifact["path"], _task.artifactsDir() )
    artifact["path"] = os.path.join(_task.artifactsDir(), os.path.basename(artifact["path"]))[heap_len:]

    obj = get_result()
    obj["artifacts"].append( artifact )
    set_result( obj )

def set_status( status ) :
    obj = get_result()
    obj["status"] = status
    set_result( obj )

# RAW LOG WRITE
def write( s, append=True ) :
    test = get_test()
    if test is None :
        if append == True :
            was = memcached.get( derive_task_log_key(), u"" )
            memcached.set( derive_task_log_key(), was + u"\n" + s )
        else :
            memcached.set( derive_task_log_key(), s )
    else :
        if append == True :
            obj = get_result()
            obj["log"] += u"\n" + s
            set_result(obj)
        else :
            obj = get_result()
            obj["log"] = s
            set_result(obj)

def get_task_log() :
    return memcached.get( derive_task_log_key(), "" )

def ajax_read( task_id=None, log_len = 0, tests_count = 0 ) :
    with current_task( int(task_id) ) :
        _task = get_task()

        if (_task.status == u"success" or _task.status == u"fail") :
            return { "state" : "final",
                     "text" : _task.log[log_len:],
                     "result" : json.loads( _task.result )[tests_count:] }

        return { "state" : "continue",
                 "text" : get_task_log()[log_len:],
                 "result" : get_all_results()[tests_count:] }

# WITH STATEMENT
class current_task:
    def __init__(self, task):
        if type(task) in (int, long) :
            self._task_id = task
        else :
            self._task_id = task.task_id

    def __enter__(self):
        global _task_id
        self._old_task = _task_id
        _task_id = self._task_id

    def __exit__(self, etype, value, traceback):
        global _task_id
        _task_id = self._old_task

class current_test:
    def __init__(self, test):
        self._test = test

    def __enter__(self):
        global _test
        self._old_test = _test
        _test = self._test

    def __exit__(self, etype, value, traceback):
        global _test
        _test = self._old_test

