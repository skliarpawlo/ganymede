from core import memcached
from core import db
from testing_runtime import models

_task = None

def set_task( task ) :
    global _task
    _task = task

def derive_task_key() :
    global _task
    if _task == None :
        return "GANY_TASK_MAIN_LOG"
    return "GANY_TASK_LOG_" + str(_task.task_id)

def write( s, task_id=None, append=True ) :
    global _task
    if not (task_id == None) :
        _task = db.session.query( models.Task ).filter( models.Task.task_id == task_id ).one()

    if append == True :
        v = memcached.get( derive_task_key() )
        if not v :
            v = ''
        memcached.set( derive_task_key(), v + "\n" + s )
    else :
        memcached.set( derive_task_key(), s )

def reset( task_id=None ) :
    write( "", task_id=task_id, append=False )


def ajax_read( task_id=None, len=0 ) :
    global _task
    if not (task_id == None) :
        _task = db.session.query( models.Task ).filter( models.Task.task_id == task_id ).one()

    if (_task.status == "SUCCESS" or _task.status == "FAIL") :
        return { "state" : "final", "text" : _task.log[len:] }

    return { "state" : "continue", "text" : memcached.get( derive_task_key() )[len:] }

def read( task_id=None ) :
    global _task
    if not (task_id == None) :
        _task = db.session.query( models.Task ).filter( models.Task.task_id == task_id ).one()

    if (_task.status == "SUCCESS" or _task.status == "FAIL") :
        return _task.log

    return memcached.get( derive_task_key() )

class task_log:
    def __init__(self, task):
        self._task = task

    def __enter__(self):
        global _task
        self._old = _task
        _task = self._task

    def __exit__(self, etype, value, traceback):
        global _task
        _task = self._old