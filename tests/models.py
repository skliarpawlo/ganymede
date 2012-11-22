from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UnicodeText, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class CheckRedirect(Base) :
    __tablename__ = 'test_check_redirects'

    source = Column(UnicodeText(255),primary_key=True)
    dest = Column(UnicodeText(255))

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

class TitleTest( Base ):
    __tablename__ = "test_seo_titles"

    domain = Column(String(64), primary_key=True)
    url = Column(UnicodeText(255), primary_key=True)
    title = Column(UnicodeText)
    h1 = Column(UnicodeText)
