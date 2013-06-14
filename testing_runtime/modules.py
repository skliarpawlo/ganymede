from core import db
from models import Module
from testlib import utils

class Dummy :
    pass

def import_modules( loc, glob ) :

    modules = db.session.query( Module ).all()

    dc = {}
    for module in modules :

        old_keys = dc.keys()

        exec module.code in dc

        if '__builtins__' in dc :
            del dc['__builtins__']

        new_keys = dc.keys()

        cur_dc = {}
        for x in new_keys :
            if not x in old_keys :
                cur_dc[ x ] = dc[ x ]

        o = Dummy()
        for x in cur_dc :
            setattr( o, x, cur_dc[x] )

        glob.update( { module.path : o } )

    return True
