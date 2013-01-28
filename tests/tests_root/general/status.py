# coding: utf-8

from core import db, browser, config, helpers, urls, mode
import urllib
import httplib
from itertools import groupby
from tests.utils import FunctionalTest
from selenium.common.exceptions import NoSuchElementException

class CheckStatusTestCase(FunctionalTest):
    "Проверяет статус страницы и редирект"

    def run(self):
        t = db.session.query(TestPagesStatus).all()
        firefox = browser.inst
        success = True
        for test in t:
            firefox.get(urls.create(test.page_domain, test.page))
            try:
                conn = httplib.HTTPConnection(urls.host(test.page_domain))
                conn.request("HEAD", urls.path(test.page_domain, test.page).encode('utf-8'))
                response = conn.getresponse()
                assert test.status_code == response.status
                if len(test.redirect_location) > 0:
                    curl = urllib.unquote(firefox.current_url.encode('utf8'))
                    url = urls.create(test.redirect_domain, test.redirect_location).encode('utf-8')
                    assert url == curl
            except AssertionError as err:
                print "FAILED (", test.test_id, ") : ", test.page, " ", test.status_code
                if "curl" in locals():
                    print "Expected location: ", url.decode('utf-8'), " Received location: ", curl.decode('utf-8')
                else:
                    print "Expected status: ", test.status_code, " Received status: ", response.status
                success = False
                browser.save()
        if not success:
            assert False

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UnicodeText, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

class TestPagesStatus(Base):
    __tablename__ = 'test_pages_status'
    test_id = Column(Integer, primary_key=True)
    page_domain = Column(UnicodeText(50))
    page = Column(UnicodeText(255))
    status_code = Column(Integer)
    redirect_domain = Column(UnicodeText(50))
    redirect_location = Column(UnicodeText(255))

