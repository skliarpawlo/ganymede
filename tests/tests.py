# coding: utf-8

from core import db, browser, config, helpers, urls
import urllib
from models import *
from itertools import groupby
from utils import FunctionalTest
from selenium.common.exceptions import NoSuchElementException

class CheckRedirectTestCase ( FunctionalTest ) :
    "Проверяет редиректы вроде www.lun.ua/wellcome -> www.lun.ua"

    def run( self ) :
        t = db.session.query(CheckRedirect).all()
        firefox = browser.inst
        success = True
        for test in t :
            firefox.get( test.source )
            try :
                curl = urllib.unquote( firefox.current_url.encode('utf8') ).decode('utf8')
                etalon = test.dest
                assert curl == etalon
                print "OK : ", test.source, " -> ", etalon
            except AssertionError as err :
                print "FAILED : ", test.source, " -> ", etalon, " really redirected to ", curl
                success = False
                browser.save()
        if not success:
            assert False

class CheckSeoTextsTestCase( FunctionalTest ) :
    "Проверяет наличие сео текстов из таблици interface_seo_texts на соответсвующих страницах"

    def run( self ) :
        firefox = browser.inst
        success = True

        t = db.session.query(SeoText).all()
        keyf = lambda x : { 'page':x.page.page, 'domain' : x.page.domain }
        t = sorted( t, key = keyf )
        for k, testgroup in groupby( t, keyf ) :

            if k['page'][0:1] == "/" :
                firefox.get( urls.create( subdomain=k['domain'], path=k['page'] ) )
            else :
                firefox.get( urls.create( subdomain=k['domain'] ) )

            for test in testgroup :
                try:
                    if ( test.type == "title" ) :
                        xpath = config.xpath[ "title" ]
                        elem = firefox.find_element_by_xpath( xpath )
                        assert elem.text == test.content
                    elif ( test.type == "description" ) :
                        xpath = config.xpath[ "description" ]
                        elem = firefox.find_element_by_xpath( xpath )
                        assert elem.get_attribute( 'content' ) == test.content
                    elif ( test.type == "footer" ) :

                        txt = firefox.page_source.encode( 'utf-8', 'ignore' )

                        ftxt = helpers.remove_html_tags( helpers.remove_new_lines( txt ) )
                        fcontent = helpers.remove_html_tags( helpers.remove_new_lines( test.content.encode( 'utf-8', 'ignore' ) ) )

                        if not(fcontent in ftxt) :
                            print fcontent
                            print ftxt
                        assert fcontent in ftxt
                    else :
                        xpath = "//willfail"
                    #print "OK : ", test.page.page
                except NoSuchElementException as err:
                    print "FAILED : ", test.page.page, " ", test.type
                    success = False
                    browser.save()
                except AssertionError as err :
                    print "FAILED : ", test.page.page, " ", test.type
                    success = False
                    browser.save()

        if not success :
            assert False

class CheckTitlesTestCase( FunctionalTest ) :
    "Проверяет соответсие тайтлов на страницах, значениям из таблици test_seo_titles"

    def run( self ) :
        firefox = browser.inst
        t = db.session.query(TitleTest).all()

        success = True

        for test in t :
            try :
                firefox.get( urls.create( subdomain=test.domain, path=test.url ) )

                xpath = config.xpath[ "title" ]
                elem = firefox.find_element_by_xpath( xpath )
                if (not elem.text == test.title) :
                    print elem.text
                    print test.title
                assert elem.text == test.title

                xpath = config.xpath[ "h1" ]
                elem = firefox.find_element_by_xpath( xpath )
                if (not elem.text == test.h1) :
                    print elem.text
                    print test.h1
                assert elem.text == test.h1

                print "OK : ", test.domain, " ", test.url
            except NoSuchElementException as err:
                print "FAILED : ", test.domain, " ", test.url
                success = False
                browser.save()
            except AssertionError as err :
                print "FAILED : ", test.domain, " ", test.url
                success = False
                browser.save()

        if not success :
            assert False