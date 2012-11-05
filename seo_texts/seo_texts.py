#!/usr/bin/env python

from selenium.common.exceptions import NoSuchElementException
import unittest

from shared import config
from shared import browser
from shared import vscreen
from models import SeoText

from itertools import groupby
from shared.helpers import *

import sys


class CheckTextTestCase( unittest.TestCase ) :
                    
    def setUp( self ) :
        vscreen.start()
        browser.start()

    def tearDown( self ) :
        browser.stop()
        vscreen.stop()
                    
    def test_texts( self ) :
        firefox = browser.inst

        heap = sys.argv[ 1 ]
        browser.setHeap( heap )
                
        t = SeoText.objects.all()
        keyf = lambda x : (x.page, x.domain)
        t = sorted( t, key = keyf )
        for k, testgroup in groupby( t, keyf ) :
        
            if k[0][0:1] == "/" :
                firefox.get("http://" + k[1] + ".lun.ua" + k[0] )
            else :
                firefox.get("http://" + k[1] + ".lun.ua" )
                
            for test in testgroup :
                try:
                    if ( test[ "type" ] == "title" ) :
                        xpath = config.xpath[ "title" ]
                        elem = firefox.find_element_by_xpath( xpath )
                        self.assertEqual( elem.text.encode( 'utf-8', 'ignore' ), test[ 'content' ] )
                    elif ( test[ "type" ] == "description" ) :
                        xpath = config.xpath[ "description" ]
                        elem = firefox.find_element_by_xpath( xpath )
                        self.assertEqual( elem.get_attribute( 'content' ).encode( 'utf-8', 'ignore' ), test[ 'content' ] )
                    elif ( test[ "type" ] == "footer" ) :
                        
                        txt = firefox.page_source.encode( 'utf-8', 'ignore' )
                        
                        ftxt = remove_html_tags( remove_new_lines( txt ) )
                        fcontent = remove_html_tags( remove_new_lines( test[ 'content' ] ) )

                        self.assertTrue( fcontent in ftxt, test[ 'page' ] )
                    else :
                        xpath = "//willfail"        
                    print "OK : ", test[ 'page' ]
                except NoSuchElementException as err:
                    print "FAILED : ", test[ "page" ], " ", test[ "type" ]
                    browser.save()                    
                except AssertionError as err :
                    print "FAILED : ", test[ "page" ], " ", test[ "type" ]
                    browser.save()

if ( __name__ == "__main__" ) :
    suite = unittest.TestLoader().loadTestsFromTestCase(CheckTextTestCase)
    unittest.TextTestRunner(verbosity=0).run(suite)
            
    
