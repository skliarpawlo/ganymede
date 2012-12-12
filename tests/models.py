from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UnicodeText, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

class TestResult(Base):
    __tablename__ = 'test_results'
    test_id = Column(UnicodeText(255), primary_key=True)
    exec_time = Column(DateTime, primary_key=True)
    domain = Column(UnicodeText(128))
    status = Column(UnicodeText(128))
    log = Column(UnicodeText)

class TestPagesStatus(Base):
    __tablename__ = 'test_pages_status'
    test_id = Column(Integer(10), primary_key=True)
    page_domain = Column(UnicodeText(50))
    page = Column(UnicodeText(255))
    status_code = Column(Integer(10))
    redirect_domain = Column(UnicodeText(50))
    redirect_location = Column(UnicodeText(255))

class CheckRedirect(Base):
    __tablename__ = 'test_check_redirects'

    source = Column(UnicodeText(255), primary_key=True)
    dest = Column(UnicodeText(255))


class Page(Base):
    __tablename__ = 'interface_pages'

    page_id = Column(Integer(10), primary_key=True)
    city_id = Column(Integer(10))
    domain = Column(String(64))
    page = Column(String(255))
    route = Column(String(64))
    params = Column(String(255))
    impressions = Column(Integer(10))


class SeoText(Base):
    __tablename__ = 'interface_seo_texts'
    page = relationship(Page)

    page_id = Column(Integer(10), ForeignKey('interface_pages.page_id'), primary_key=True)
    type = Column(String(50), primary_key=True)
    content = Column(UnicodeText)


class TitleTest(Base):
    __tablename__ = "test_seo_titles"

    domain = Column(String(64), primary_key=True)
    url = Column(UnicodeText(255), primary_key=True)
    title = Column(UnicodeText)
    h1 = Column(UnicodeText)
