from core import db, browser, config, helpers
import urllib
from models import *
from itertools import groupby
from utils import FunctionalTest
from selenium.common.exceptions import NoSuchElementException

import unittest
class FakeTestCase(unittest.TestCase) :
    def test_fake(self):
        print('FAKE TEST LOG')

class CheckRedirectTestCase ( FunctionalTest ) :

    id = "check_redirects"

    def test_redirects( self ) :
        t = db.session.query(CheckRedirect).all()
        firefox = browser.inst
        success = True
        for test in t :
            firefox.get( test.source )
            try :
                curl = urllib.unquote( firefox.current_url.encode('utf8') ).decode('utf8')
                etalon = test.dest
                self.assertEqual( curl, etalon )
                print( "OK : ", test.source, " -> ", etalon )
            except AssertionError as err :
                print( "FAILED : ", test.source, " -> ", etalon, " really redirected to ", curl )
                success = False
                browser.save()
        if not success:
            raise Exception('Test failed')

class CheckSeoTextsTestCase( FunctionalTest ) :

    id = 'seo_texts'

    def test_texts( self ) :
        firefox = browser.inst
        success = True

        t = db.session.query(SeoText).all()
        keyf = lambda x : { 'page':x.page.page, 'domain' : x.page.domain }
        t = sorted( t, key = keyf )
        for k, testgroup in groupby( t, keyf ) :

            if k['page'][0:1] == "/" :
                firefox.get("http://" + k['domain'] + ".lun.ua" + k['page'] )
            else :
                firefox.get("http://" + k['domain'] + ".lun.ua" )

            for test in testgroup :
                try:
                    if ( test.type == "title" ) :
                        xpath = config.xpath[ "title" ]
                        elem = firefox.find_element_by_xpath( xpath )
                        self.assertEqual( elem.text, test.content )
                    elif ( test.type == "description" ) :
                        xpath = config.xpath[ "description" ]
                        elem = firefox.find_element_by_xpath( xpath )
                        self.assertEqual( elem.get_attribute( 'content' ), test.content )
                    elif ( test.type == "footer" ) :

                        txt = firefox.page_source.encode( 'utf-8', 'ignore' )

                        ftxt = helpers.remove_html_tags( helpers.remove_new_lines( txt ) )
                        fcontent = helpers.remove_html_tags( helpers.remove_new_lines( test.content.encode( 'utf-8', 'ignore' ) ) )

                        self.assertTrue( fcontent in ftxt, test.page )
                    else :
                        xpath = "//willfail"
                    print "OK : ", test.page.page
                except NoSuchElementException as err:
                    print "FAILED : ", test.page.page, " ", test.type
                    success = False
                    browser.save()
                except AssertionError as err :
                    print "FAILED : ", test.page.page, " ", test.type
                    success = False
                    browser.save()

        if not success :
            self.assertTrue( False, 'Test failed' )

class CheckTitlesTestCase( FunctionalTest ) :

    id = "urls_titles"

    def test_titles( self ) :
        firefox = browser.inst
        t = db.session.query(TitleTest).all()

        success = True

        for test in t :
            try :
                firefox.get( "http://" + test.domain + ".lun.ua" + test.url )

                xpath = config.xpath[ "title" ]
                elem = firefox.find_element_by_xpath( xpath )
                self.assertEqual( elem.text, test.title )

                xpath = config.xpath[ "h1" ]
                elem = firefox.find_element_by_xpath( xpath )
                self.assertEqual( elem.text, test.h1 )

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
                raise Exception('Test failed')