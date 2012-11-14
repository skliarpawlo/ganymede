import core.db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship

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
    page = relationship(Page)

    page_id = Column(Integer(10), ForeignKey('interface_pages.page_id'), primary_key=True)
    type = Column(String(50), primary_key=True)
    content = Column(UnicodeText)

if __name__ == '__main__' :
    core.db.init()
    data = core.db.session.query(SeoText).all()
    for x in data :
        print(x.page.route)
    core.db.session.close()