#!/usr/bin/env python
# coding: utf-8

import unittest
from shared import db, browser, vscreen
import urllib
import sys

class CheckRedirect ( unittest.TestCase ) :

    def setUp( self ) :
        vscreen.start()
        browser.start()
        db.connect()        

    def testRedirects( self ) :
    
        self.maxDiff = None
        
        browser.setHeap( sys.argv[ 1 ] )
    
        t = db.createCommand( "SELECT * FROM test_check_redirects" ).queryAll()
        
        firefox = browser.inst
    
        for test in t :
    
            firefox.get( test[ "source" ] )
            try :
                curl = urllib.unquote( firefox.current_url.encode( "utf-8" ) )
                etalon = test[ "dest" ]
            
                self.assertEqual( curl, etalon )
                print( "OK : " + test[ "source" ] + " -> " + etalon )
            except AssertionError as err :
                print( "FAILED : " + test[ "source" ] + " -> " + etalon + " really redirected to " + curl )
                browser.save()
    

    def tearDown( self ) :
        browser.stop()
        vscreen.stop()
        db.close()
    
if ( __name__ == '__main__' ) :
    suite = unittest.TestLoader().loadTestsFromTestCase(CheckRedirect)
    unittest.TextTestRunner(verbosity=0).run(suite)




