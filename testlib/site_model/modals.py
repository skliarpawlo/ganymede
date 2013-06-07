class Modal :

    def __init__(self, ff):
        self.ff = ff

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

    def open(self):
        self.ff.find_element_by_xpath( self.own_selectors[ "open" ] ).click()

    def fill(self, key, content):
        el = self.ff.find_element_by_xpath( self.own_selectors[ key ] )
        el.clear()
        el.send_keys( content )

    def get_value(self, key):
        el = self.ff.find_element_by_xpath( self.own_selectors[ key ] )
        return el.get_attribute('value')

    def submit(self):
        self.ff.find_element_by_xpath( self.own_selectors[ "submit" ] ).click()

    def close(self):
        self.ff.find_element_by_xpath( self.own_selectors[ "close" ] ).click()

