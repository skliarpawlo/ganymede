# coding: utf-8

from selenium.webdriver.support.ui import WebDriverWait
import utils

class Page :
    url = ''

    def __init__( self, ff ):
        self.ff = ff
        self.selectors = {}

    def wait_for( self, key, sec=10 ) :
        WebDriverWait( self.ff, sec ).until(
            lambda ff :
                ff.find_element_by_xpath( self.selectors[ key ] )
        )

    def wait_page(self, sec=5 ):
        WebDriverWait( self.ff, sec ).until(
            lambda ff :
                self.url in ff.current_url
        )



class LunMainPage( Page ) :
    url = u'http://www.lun.ua/'


class NovostroykiMainPage( Page ) :
    url = u'http://novostroyki.lun.ua/'


class LunSearchPage( Page ) :
    pass


class NovostroykiSearchPage( Page ) :
    pass


class RegistrationPage( Page ) :
    own_selectors = {
        "go_to_search" : "//*[@id='static-content']//*[@href]"
    }

    def __init__(self, ff):
        Page.__init__( self, ff )
        utils.merge( self.selectors, RegistrationPage.own_selectors )

    def go_to_search(self):
        self.wait_for( "go_to_search" )
        self.ff.by_x( self.selectors[ "go_to_search" ] ).click()


