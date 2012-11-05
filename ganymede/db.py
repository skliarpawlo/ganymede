from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

_engine = None
_Session = None
session = None

def init():
    global _engine, _Session, session
    if _engine == None :
        _engine = create_engine('mysql+mysqldb://root@localhost/ganymede', pool_recycle=1800)
        _Session = sessionmaker(bind=_engine)
        session = _Session()
        print( 'init' )
