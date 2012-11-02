#!/usr/bin/env python
# coding=utf8

from selenium.common.exceptions import NoSuchElementException
import unittest

from shared import config
from shared import db
from shared import browser
from shared import vscreen
from shared.helpers import *

import os
import json
import sys

class CheckTitlesTestCase( unittest.TestCase ) :

    def setUp( self ) :
        vscreen.start()
        browser.start()
        db.connect()
        
    def tearDown( self ) :
        browser.stop()
        db.close()
        vscreen.stop()
                    
    def test_titles( self ) :
        firefox = browser.inst
        com = db.createCommand( "SELECT * FROM test_seo_titles" )
        t = com.queryAll()        
        
        heap = sys.argv[ 1 ]
        browser.setHeap( heap )
        #f = open( os.path.abspath( heap + '/urls_titles.json' ), 'r' )
        #t = json.loads( f.read() )
        #f.close()
        
        for test in t :
            try :
                firefox.get( "http://" + test[ "domain" ] + ".lun.ua" + test[ "url" ] )
                
                xpath = config.xpath[ "title" ]
                elem = firefox.find_element_by_xpath( xpath )
                self.assertEqual( elem.text.encode( "utf-8" ), test[ 'title' ] )

                xpath = config.xpath[ "h1" ]
                elem = firefox.find_element_by_xpath( xpath )
                self.assertEqual( elem.text.encode( "utf-8" ), test[ 'h1' ] )
                
                print "OK : ", test[ "domain" ], " ", test[ "url" ]
            except NoSuchElementException as err:
                print "FAILED : ", test[ "domain" ], " ", test[ "url" ]
                browser.save()
            except AssertionError as err :
                print "FAILED : ", test[ "domain" ], " ", test[ "url" ]
                browser.save()
        
if ( __name__ == "__main__" ) :
    suite = unittest.TestLoader().loadTestsFromTestCase(CheckTitlesTestCase)
    unittest.TextTestRunner(verbosity=0).run(suite)
        
