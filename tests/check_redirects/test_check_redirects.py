#!/usr/bin/env python
# coding: utf-8

import unittest
from core import db, browser
import urllib
from tests.check_redirects.models import CheckRedirect
import tests.utils

class CheckRedirectTestCase ( tests.utils.FunctionalTest ) :

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

if ( __name__ == '__main__' ) :
    suite = unittest.TestLoader().loadTestsFromTestCase(CheckRedirectTestCase)
    unittest.TextTestRunner(verbosity=0).run(suite)




