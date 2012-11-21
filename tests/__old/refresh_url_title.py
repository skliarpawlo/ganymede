#!/usr/bin/env python

from selenium.common.exceptions import NoSuchElementException

from core import browser, config, vscreen, db

import sys

heap = sys.argv[ 1 ]

try :
    vscreen.start()
    browser.start()
    db.connect()

    com = db.createCommand( "SELECT * FROM test_seo_titles" )
    t = com.queryAll()        
    
    for test in t :    
        firefox = browser.inst
        firefox.get( "http://" + test["domain"] + ".lun.ua" + test[ "url" ] )
        title = firefox.find_element_by_xpath( config.xpath[ "title" ] ).text.encode( 'utf-8' )
        h1 = firefox.find_element_by_xpath( config.xpath[ "h1" ] ).text.encode( 'utf-8' )
        db.createCommand( "UPDATE test_seo_titles SET title='{title}', h1='{h1}' WHERE domain='{domain}' AND url='{url}'".format( 
            domain = test["domain"], url = test["url"], title = title, h1 = h1 ) ).execute()
            
finally :
    browser.stop()
    vscreen.stop()
    db.close()
