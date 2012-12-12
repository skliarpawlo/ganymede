# coding: utf-8

from core import db, browser, config, helpers, urls
import urllib
import httplib
from models import *
from itertools import groupby
from utils import FunctionalTest
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy.sql import not_

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
                conn.request("HEAD", urls.path(test.page_domain, test.page.encode('utf-8')))
                response = conn.getresponse()
                assert test.status_code == response.status
                if len(test.redirect_location) > 0:
                    #проверяем редирект Location
                    curl = response.getheader('Location')
                    url = urls.create(test.redirect_domain, test.redirect_location).encode('utf-8')
                    if url.endswith('/') and not curl.endswith('/'):
                        curl += '/'
                    assert url == curl
                    #проверяем финальный Location, на случай если было несколько редиректов
                    curl = urllib.unquote(firefox.current_url.encode('utf8')).decode('utf-8')
                    assert urls.create(test.redirect_domain, test.redirect_location) == curl
                    #print "OK : ", url, " -> ", curl
                #else:
                    #print "OK : ", url, " -> ", test.status_code
            except AssertionError as err:
                print "FAILED (", test.test_id, ") : ", test.page, " ", test.status_code
                if "curl" in locals():
                    print "Expected location: ", url, " Received location: ", curl
                else:
                    print "Expected status: ", test.status_code, " Received status: ", response.status
                success = False
                browser.save()
        if not success:
            assert False

class CheckSeoTextsTestCase(FunctionalTest):
    "Проверяет наличие сео текстов из таблици interface_seo_texts на соответсвующих страницах"

    def run( self ):
        firefox = browser.inst
        success = True

        t = db.session.query(SeoText).filter(not SeoText.page.domain=='odessa')
        keyf = lambda x: {'page': x.page.page, 'domain': x.page.domain}
        t = sorted(t, key=keyf)
        for k, testgroup in groupby(t, keyf):
            if k['page'][0:1] == "/":
                firefox.get(urls.create(subdomain=k['domain'], path=k['page']))
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

                        if not(fcontent in ftxt):
                            print fcontent
                            print ftxt
                        assert fcontent in ftxt
                    else:
                        xpath = "//willfail"
                    #print "OK : ", test.page.page
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


class CheckTitlesTestCase(FunctionalTest):
    "Проверяет соответствие тайтлов на страницах, значениям из таблици test_seo_titles"

    def run( self ):
        firefox = browser.inst
        t = db.session.query(TitleTest).all()

        success = True

        for test in t:
            try:
                firefox.get(urls.create(subdomain=test.domain, path=test.url))

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

                #print "OK : ", test.domain, " ", test.url
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