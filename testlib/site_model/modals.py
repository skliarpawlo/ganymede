# coding: utf-8

import utils


class Modal :

    def __init__(self, ff):
        self.ff = ff
        self.selectors = {}

    def open(self):
        pass

    def fill(self, key, content):
        pass

    def get_value(self, key):
        pass

    def submit(self):
        pass

    def close(self):
        pass


class ProblemOnSiteModal( Modal ) :

    own_selectors = {
        "open" : "//*[@id='problembut']",
        "message" : "//*[@id='problemText']",
        "email" : "//*[@id='problemEmail']",
        "submit" : "//*[@id='problemButton']",
        "close" : "//*[@id='problembut-box']//*[contains(@class,'closebut')]"
    }

    def __init__(self, ff):
        Modal.__init__( self, ff )
        utils.merge( self.selectors, ProblemOnSiteModal.own_selectors )

    def open(self):
        self.ff.by_x( self.selectors[ "open" ] ).click()

    def fill(self, key, content):
        el = self.ff.by_x( self.selectors[ key ] )
        el.clear()
        el.send_keys( content )

    def get_value(self, key):
        el = self.ff.by_x( self.selectors[ key ] )
        return el.get_attribute('value')

    def submit(self):
        self.ff.by_x( self.selectors[ "submit" ] ).click()

    def close(self):
        self.ff.by_x( self.selectors[ "close" ] ).click()

