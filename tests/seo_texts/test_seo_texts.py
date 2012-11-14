#!/usr/bin/env python
# coding: utf-8

from selenium.common.exceptions import NoSuchElementException
import unittest

from core import db
from core import config
from core import browser
from core import helpers
from tests.seo_texts.models import SeoText
import tests.utils

from itertools import groupby

class CheckTextTestCase( tests.utils.FunctionalTest ) :

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

if (__name__=="__main__"):
    unittest.main()