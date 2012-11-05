import ganymede.db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Page( Base ) :
    __tablename__ = 'interface_pages'

    page_id = Column(Integer(10), primary_key=True)
    city_id = Column(Integer(10))
    domain = Column(String(64))
    page = Column(String(255))
    route = Column(String(64))
    params = Column(String(255))
    impressions = Column(Integer(10))

class SeoText( Base ) :
    __tablename__ = 'interface_seo_texts'

    page_id = Column(Integer(10), primary_key=True)
    type = Column(String(50), primary_key=True)
    content = Column(String)

if __name__ == '__main__' :
    ganymede.db.init()
    data = ganymede.db.session.query(SeoText).all()
    for x in data :
        print(x.content)
    ganymede.db.session.close()