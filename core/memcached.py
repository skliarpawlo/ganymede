import memcache

session = None

def init() :
    global session
    session = memcache.Client(['127.0.0.1:11211'],debug=0)

def set( key, val ) :
    global session
    if ( session == None ) :
        init()
    session.set( key, val )

def get( key, default_val=None ) :
    global session
    if ( session == None ) :
        init()
    val = session.get( key )
    if val is None :
        return default_val
    else :
        return val
