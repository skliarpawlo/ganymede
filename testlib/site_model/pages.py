# coding: utf-8

from selenium.webdriver.support.ui import WebDriverWait
import utils
import urllib

class Page :
    def __init__( self, ff, url='' ):
        self.ff = ff
        self.selectors = {}
        self.url = url

    def wait_for( self, key, sec=10 ) :
        WebDriverWait( self.ff, sec ).until(
            lambda ff :
                ff.find_element_by_xpath( self.selectors[ key ] )
        )

    def wait_page(self, sec=5 ):
        WebDriverWait( self.ff, sec ).until(
            lambda ff :
                self.url in Page.url_unquote( ff.current_url ),
                u"Не дождались подгрузки страницы '{0}'".format( self.url ).encode( "utf-8" )
        )

    @staticmethod
    def url_unquote(url) :
        return urllib.unquote( url.encode('utf-8') ).decode('utf-8')


class LunMainPage( Page ) :
    def __init__(self, ff):
        Page.__init__( self, ff, u'http://www.lun.ua/' )


class NovostroykiMainPage( Page ) :
    def __init__(self, ff):
        Page.__init__( self, ff, u'http://novostroyki.lun.ua/' )


class LunSearchPage( Page ) :
    pass


class NovostroykiSearchPage( Page ) :
    pass


class RegistrationPage( Page ) :
    own_selectors = {
        "go_to_search" : "//*[@id='static-content']//*[@href]"
    }

    def __init__(self, ff):
        Page.__init__( self, ff, u"http://www.lun.ua/register" )
        utils.merge( self.selectors, RegistrationPage.own_selectors )

    def go_to_search(self):
        self.wait_for( "go_to_search" )
        self.ff.by_x( self.selectors[ "go_to_search" ] ).click()


class BigmirFrame( Page ) :
    own_selectors = {
        "iframe" : "//*[@id='lun-iframe']",
        "blocks" : {
            "buildings" : '//*[@id="buildings-block"]',
            "results" : '//*[@id="result-stream"]',
        },
        "results" : '//*[@id="result-stream"]//*[contains(@class,"stream-item")]',
        "pagination" : {
            "2" : "//*[contains(@href,'page=2') and contains(@href,'lun.ua')]",
            "3" : "//*[contains(@href,'page=3') and contains(@href,'lun.ua')]"
        }
    }

    def __init__( self, ff ):
        Page.__init__( self, ff, u"http://finance.bigmir.net/realty/lun" )
        utils.merge( self.selectors, BigmirFrame.own_selectors )

