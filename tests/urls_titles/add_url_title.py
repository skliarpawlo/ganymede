#!/usr/bin/env python

from selenium.common.exceptions import NoSuchElementException

from core import browser, config, vscreen, db

import sys

heap = sys.argv[ 1 ]
www = sys.argv[ 2 ]
url = sys.argv[ 3 ]

try :
    vscreen.start()
    browser.start()
    db.connect()    

    firefox = browser.inst
    firefox.get( "http://" + www + ".lun.ua" + url )
    
    title = firefox.find_element_by_xpath( config.xpath[ "title" ] ).text.encode('utf-8')
    h1 = firefox.find_element_by_xpath( config.xpath[ "h1" ] ).text.encode('utf-8')
    
    db.createCommand( "INSERT INTO test_seo_titles (domain,url,title,h1) VALUES ('{domain}','{url}','{title}','{h1}') ON DUPLICATE KEY UPDATE  title='{title}', h1='{h1}'".format ( domain=www,url=url,title=title,h1=h1 ) ).execute()
        
finally :
    browser.stop()
    vscreen.stop()
    db.close()
    
