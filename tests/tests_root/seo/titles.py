# coding: utf-8

from core import db, browser, config, helpers, urls, mode
import urllib
import httplib
from itertools import groupby
from tests.utils import FunctionalTest
from selenium.common.exceptions import NoSuchElementException

class CheckTitlesTestCase(FunctionalTest):
    "Проверяет соответствие тайтлов на страницах, значениям из таблици test_seo_titles"

    def run( self ):
        firefox = browser.inst
        t = db.session.query(TitleTest).all()

        success = True

        for test in t:
            try:
                firefox.get(urls.create(test.domain, test.url))

                xpath = config.xpath["title"]
                elem = firefox.find_element_by_xpath(xpath)
                if (not elem.text == test.title):
                    print elem.text
                    print test.title
                assert elem.text == test.title

                xpath = config.xpath["h1"]
                elem = firefox.find_element_by_xpath(xpath)
                if (not elem.text == test.h1):
                    print elem.text
                    print test.h1
                assert elem.text == test.h1
            except NoSuchElementException as err:
                print "FAILED : ", test.domain, " ", test.url
                success = False
                browser.save()
            except AssertionError as err:
                print "FAILED : ", test.domain, " ", test.url
                success = False
                browser.save()

        if not success:
            assert False

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UnicodeText, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

class TitleTest(Base):
    __tablename__ = "test_seo_titles"

    domain = Column(String(64), primary_key=True)
    url = Column(UnicodeText(255), primary_key=True)
    title = Column(UnicodeText)
    h1 = Column(UnicodeText)
