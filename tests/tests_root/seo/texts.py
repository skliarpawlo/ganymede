# coding: utf-8

from core import db, browser, config, helpers, urls, mode
import urllib
import httplib
from itertools import groupby
from tests.utils import FunctionalTest
from selenium.common.exceptions import NoSuchElementException

class CheckSeoTextsTestCase(FunctionalTest):
    "Проверяет наличие сео текстов из таблици interface_seo_texts на соответсвующих страницах"

    def run( self ):
        firefox = browser.inst
        success = True

        if (mode.complete == mode.COMPLETENESS_FULL) :
            t = db.session.query(SeoText)
        else :
            t = db.session.query(SeoText).limit(3)

        keyf = lambda x: {'page': x.page.page, 'domain': x.page.domain}
        t = sorted(t, key=keyf)
        for k, testgroup in groupby(t, keyf):
            if k['page'][0:1] == "/":
                firefox.get(urls.create(k['domain'], k['page']))
            else:
                firefox.get(urls.create(subdomain=k['domain']))

            for test in testgroup:
                try:
                    if ( test.type == "title" ):
                        xpath = config.xpath["title"]
                        elem = firefox.find_element_by_xpath(xpath)
                        assert elem.text == test.content
                    elif ( test.type == "description" ):
                        xpath = config.xpath["description"]
                        elem = firefox.find_element_by_xpath(xpath)
                        assert elem.get_attribute('content') == test.content
                    elif ( test.type == "footer" ):
                        txt = firefox.page_source.encode('utf-8', 'ignore')

                        ftxt = helpers.remove_html_tags(helpers.remove_new_lines(txt))
                        fcontent = helpers.remove_html_tags(
                            helpers.remove_new_lines(test.content.encode('utf-8', 'ignore')))

                        assert fcontent in ftxt
                    else:
                        xpath = "//willfail"
                except NoSuchElementException as err:
                    print "FAILED : ", test.page, " ", test.type
                    success = False
                    browser.save()
                except AssertionError as err:
                    print "FAILED : ", test.page.page, " ", test.type.encode
                    success = False
                    browser.save()

        if not success:
            assert False

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UnicodeText, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

class Page(Base):
    __tablename__ = 'interface_pages'

    page_id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    domain = Column(String(64))
    page = Column(String(255))
    route = Column(String(64))
    params = Column(String(255))
    impressions = Column(Integer)

class SeoText(Base):
    __tablename__ = 'interface_seo_texts'
    page = relationship(Page)

    page_id = Column(Integer, ForeignKey('interface_pages.page_id'), primary_key=True)
    type = Column(String(50), primary_key=True)
    content = Column(UnicodeText)

