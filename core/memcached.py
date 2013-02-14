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

def get( key ) :
    global session
    if ( session == None ) :
        init()
    return session.get( key )
