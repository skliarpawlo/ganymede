# coding: utf-8

import utils


class Form :
    own_selectors = {}

    def __init__(self,ff):
        self.ff = ff
        self.selectors = {}

    def get(self, key):
        return self.ff.by_x(self.selectors[ key ])

    def fill(self, key, value):
        self.ff.by_x( self.selectors[ key ] ).send_keys( value )

    def submit(self):
        self.get( "submit" ).click()


class LoginForm( Form ) :
    own_selectors = {
        "open" : "//*[@id='user-menu']//*[@class='auth-right']",
        "register" : "//*[@id='user-menu']//a[@href='/register']",
        "user_name" : "//*[@id='auth-email']",
        "user_password" : "//*[@id='auth-pass']",
        "login" : "//*[@id='auth-but']",
        "logout" : "//*[@id='user-menu']//*[contains(@class, 'logout-but')]"
    }

    def __init__(self, ff):
        Form.__init__(self,ff)
        utils.merge( self.selectors, LoginForm.own_selectors )


    def open(self):
        if utils.element_present( self.ff, self.selectors[ "login" ] ) :
            if not self.ff.by_x( self.selectors[ "login" ] ).is_displayed() :
                self.ff.by_x( self.selectors[ "open" ] ).click()
        if utils.element_present( self.ff, self.selectors[ "logout" ] ) :
            if not self.ff.by_x( self.selectors[ "logout" ] ).is_displayed() :
                self.ff.by_x( self.selectors[ "open" ] ).click()

    def close(self):
        if utils.element_present( self.ff, self.selectors[ "login" ] ) :
            if self.ff.by_x( self.selectors[ "login" ] ).is_displayed() :
                self.ff.by_x( self.selectors[ "open" ] ).click()
        if utils.element_present( self.ff, self.selectors[ "logout" ] ) :
            if self.ff.by_x( self.selectors[ "logout" ] ).is_displayed() :
                self.ff.by_x( self.selectors[ "open" ] ).click()

    def login(self, user_name, user_password ) :
        self.open()
        self.fill( "user_name", user_name )
        self.fill( "user_password", user_password )
        self.ff.by_x( self.selectors[ "login" ] ).click()

    def logout(self):
        self.open()
        self.ff.by_x( self.selectors[ "logout" ] ).click()



class RegistrationForm( Form ) :
    own_selectors = {
        "user_name" : "//input[@name='email']",
        "user_password" : "//input[@name='pass']",
        "submit" : "//input[@id='register-but']"
    }

    def __init__(self, ff):
        Form.__init__(self,ff)
        utils.merge( self.selectors, RegistrationForm.own_selectors )

