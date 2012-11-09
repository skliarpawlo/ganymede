import core.db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UnicodeText

Base = declarative_base()

class CheckRedirect(Base) :
    __tablename__ = 'test_check_redirects'

    source = Column(UnicodeText(255),primary_key=True)
    dest = Column(UnicodeText(255))

if (__name__=='__main__'):
    core.db.init()
    t = core.db.session.query(CheckRedirect).all()
    for x in t :
        print(x.source + " -> " + x.dest)
    core.db.session.close()