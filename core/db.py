from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

_engine = None
_Session = None
session = None

def init():
    global _engine, _Session, session
    if _engine == None :
        #_engine = create_engine('mysql+mysqldb://root@localhost/ganymede?charset=utf8', pool_recycle=1800)
        _engine = create_engine('mysql+mysqldb://skliar:lilipad@77.120.117.134/lun_ua_new?charset=utf8', pool_recycle=0)
        _Session = sessionmaker(bind=_engine)
        session = _Session()

def close():
    global session
    session.commit()
    session.close()