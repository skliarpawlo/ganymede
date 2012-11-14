#!/usr/bin/env python
# coding=utf8

from selenium.common.exceptions import NoSuchElementException

from core import config, browser, db
from tests.urls_titles.models import TitleTest
import tests.utils
import unittest

class CheckTitlesTestCase( tests.utils.FunctionalTest ) :

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

if (__name__=='__main__'):
    unittest.main()