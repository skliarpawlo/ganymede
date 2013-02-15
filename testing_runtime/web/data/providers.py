from core import db
from testing_runtime import models

def tasks( params={} ) :

    limit = 10
    if params.has_key('pagesize') :
        limit = int(params['pagesize'])

    offset = 0
    if params.has_key('page') :
        offset = (int(params['page']) - 1) * limit

    return db.session.query( models.Task )\
    .order_by( models.Task.add_time.desc() )\
    .offset(offset)\
    .limit(limit)
