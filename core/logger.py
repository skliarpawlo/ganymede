from core import memcached
from core import db
from core import path
from testing_runtime import models
import json
import os
import ganymede.settings

_task_id = None

def get_task( task_id=None ) :
    global _task_id
    if task_id is None :
        task_id = _task_id
    return db.session.query( models.Task ).filter( models.Task.task_id == task_id ).one()

def set_task( task ) :
    global _task_id
    _task_id = task.task_id

def derive_task_log_key( task_id=None ) :
    _task = get_task( task_id )
    if _task == None :
        return "GANY_TASK_MAIN_LOG"
    return "GANY_TASK_LOG_" + str(_task.task_id)

def derive_task_artifacts_key( task_id=None ) :
    _task = get_task( task_id )
    if _task == None :
        return "GANY_TASK_MAIN_ARTIFACTS"
    return "GANY_TASK_ARTIFACTS_" + str(_task.task_id)

def add_artifact( artifact, task_id=None ) :
    _task = get_task( task_id )

    heap_len = len(ganymede.settings.HEAP_PATH)
    path.copy( artifact["path"], _task.artifactsDir() )
    artifact["path"] = os.path.join(_task.artifactsDir(), os.path.basename(artifact["path"]))[heap_len:]

    artis = json.loads( memcached.get( derive_task_artifacts_key(task_id), u"[]" ) )
    artis.append( artifact )
    memcached.set( derive_task_artifacts_key(task_id), json.dumps( artis ) )

def get_artifacts(task_id = None) :
    _task = get_task( task_id )

    if (_task.status == u"success" or _task.status == u"fail") :
        return json.loads( _task.artifacts )

    return json.loads( memcached.get( derive_task_artifacts_key( task_id ) ) )

def write( s, task_id=None, append=True ) :
    if append == True :
        v = memcached.get( derive_task_log_key(task_id) )
        if not v :
            v = ''
        memcached.set( derive_task_log_key(task_id), v + "\n" + s )
    else :
        memcached.set( derive_task_log_key(task_id), s )

def reset( task_id=None ) :
    write( "", task_id=task_id, append=False )
    memcached.set( derive_task_artifacts_key(task_id), u"[]" )

def ajax_read( task_id=None, len=0, artifacts_count=0 ) :
    _task = get_task( task_id )

    if (_task.status == u"success" or _task.status == u"fail") :
        return { "state" : "final",
                 "text" : _task.log[len:],
                 "artifacts" : json.loads( _task.artifacts )[artifacts_count:] }

    return { "state" : "continue",
             "text" : memcached.get( derive_task_log_key(task_id), "" )[len:],
             "artifacts" : json.loads( memcached.get( derive_task_artifacts_key(task_id) ) )[artifacts_count:]}

def read( task_id=None ) :
    _task = get_task( task_id )

    if (_task.status == u"success" or _task.status == u"fail") :
        return _task.log

    return memcached.get( derive_task_log_key(task_id) )

class task_log:
    def __init__(self, task):
        self._task_id = task.task_id

    def __enter__(self):
        global _task_id
        self._old = _task_id
        _task_id = self._task_id

    def __exit__(self, etype, value, traceback):
        global _task_id
        _task_id = self._old