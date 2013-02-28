from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import ganymede.settings
import json
import os

config = json.loads(
    open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "config",
            ganymede.settings.MODE,
            "db.json"
        ),
        "r" ).read()
)

_engine = None
_Session = None
session = None

def init():
    global _engine, _Session, session, config
    if _engine == None :
        _engine = create_engine(config["connection"], pool_size=3, pool_recycle=30)
        _Session = sessionmaker(bind=_engine)
    session = _Session()

def reconnect():
    global session, _Session
    if not session is None :
        try :
            session.commit()
        except :
            session.rollback()
    session = _Session()

def execute(sql):
    global _engine
    return _engine.execute(sql)

def close():
    global session
    try :
        session.commit()
    except :
        session.rollback()
        raise
    finally:
        session = None