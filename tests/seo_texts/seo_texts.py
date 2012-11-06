#!/usr/bin/env python
# coding: utf-8

from selenium.common.exceptions import NoSuchElementException
import unittest

import core.db
from core import config
from core import browser
from core import vscreen
from tests.seo_texts.models import SeoText

from itertools import groupby
from core.helpers import *

class CheckTextTestCase( unittest.TestCase ) :
                    
    def setUp( self ) :
        vscreen.start()
        browser.start()

    def tearDown( self ) :
        browser.stop()
        vscreen.stop()
                    
    def test_texts( self ) :
        firefox = browser.inst

        heap = 'heap'
        browser.setHeap( heap )

        success = True
                
        t = core.db.session.query(SeoText).all()
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
                        
                        ftxt = remove_html_tags( remove_new_lines( txt ) )
                        fcontent = remove_html_tags( remove_new_lines( test.content.encode( 'utf-8', 'ignore' ) ) )

                        self.assertTrue( fcontent in ftxt, test.page )
                    else :
                        xpath = "//willfail"        
                    print "OK : ", test.page.page
                except NoSuchElementException as err:
                    print "FAILED : ", test.page.page, " ", test.type
                    browser.save()                    
                except AssertionError as err :
                    print "FAILED : ", test.page.page, " ", test.type
                    success = False
                    browser.save()

        if not success :
            self.assertTrue( False, u'Были фейлы' )

if ( __name__ == "__main__" ) :
    core.db.init()
    suite = unittest.TestLoader().loadTestsFromTestCase(CheckTextTestCase)
    unittest.TextTestRunner(verbosity=0).run(suite)
    core.db.session.close()
            
    
