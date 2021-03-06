# coding: utf-8

from core import browser
from core import vscreen
from core import path
from core import logger
from core import db
from testing_runtime.web.decorators import html
import time
import re
import os
import traceback
import ganymede.settings
import httplib
from urlparse import urlparse
import urllib
from testing_runtime.web.decorators import html
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


heap_dir = ganymede.settings.HEAP_PATH
base_dir = ganymede.settings.BASE_PATH


class Test( object ):

    def setUp(self):
        path.ensure( self.testDir() )

        path.clean( self.artifactsDir() )
        path.ensure( self.artifactsDir() )

        db.reconnect()

    def tearDown(self):
        pass

    def testDir(self) :
        return os.path.join(heap_dir, "tests", test_name(self))

    def pidFile(self) :
        return os.path.join(heap_dir, "tests", test_name(self), "lock.pid")

    def artifactsDir(self):
        return os.path.join(self.testDir(), "photos")


class MainTest(Test) :

    def run(self):
        logger.write( u"Running test '{0}'".format( self.__doc__.decode("utf-8") ) )

    def snapshot(self):
        pass


class RedirectTest(MainTest) :

    # [ [ url, redirect_status, to_url, to_status ],... ]
    redirects = []

    def run(self):
        super(RedirectTest, self).run()

        for (from_url, redirect_status, dest_url, dest_status) in self.redirects :

            parsed_url = urlparse( from_url )
            conn = httplib.HTTPConnection( parsed_url.netloc )
            conn.request( "HEAD", parsed_url.path.encode('utf-8') )
            from_response = conn.getresponse()

            assert from_response.status == redirect_status, \
            u"При посещении страницы {0}, ожидался {1} переход на страницу {2}, но получен статус {3}".\
            format( html.link(from_url,from_url), redirect_status, html.link( dest_url, dest_url ), from_response.status )

            loc = from_response.getheader('location').decode('utf-8')

            assert loc == dest_url, \
            u"При посещении страницы {0}, ожидался {1} переход на страницу {2}, но редирект перевел на страницу {3}".\
            format( html.link(from_url,from_url), redirect_status, html.link( dest_url, dest_url ), html.link( loc, loc ) )

            parsed_url2 = urlparse( loc )
            conn2 = httplib.HTTPConnection( parsed_url2.netloc )
            conn2.request( "HEAD", parsed_url2.path.encode('utf-8') )
            dest_response = conn2.getresponse()

            assert dest_response.status == dest_status,\
            u"При посещении страницы {0}, ожидался {1} переход на страницу {2} со статусом {3}, но получен статус {4}".\
            format( html.link(from_url,from_url), redirect_status, html.link( dest_url, dest_url ), dest_status, dest_response.status )


class FunctionalTest(MainTest) :

    browser = None

    def setUp(self):
        super(FunctionalTest, self).setUp()

        # functional tests setup
        vscreen.start()
        browser.start()
        browser.setHeap(self.artifactsDir())
        self.browser = browser.inst

    def tearDown(self):
        self.browser = None

        browser.stop()
        vscreen.stop()

        super(FunctionalTest, self).tearDown()

    def snapshot(self):
        snapshot()


class SeleniumIDETest( FunctionalTest ) :

    def setUp(self):
        super(SeleniumIDETest, self).setUp()
        self.browser.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True

    def assertEqual(self, need, have):
        need = to_unicode( need )
        have =  to_unicode( have )
        assert need == have, u"Error: {0} != {1}".format( need, have )

    def assertRegexpMatches(self, text, regexp, msg=None) :
        text = to_unicode( text )
        regexp = to_unicode( regexp )
        x = re.compile(regexp)
        assert x.search(text), u"Не найден {0} по регулярке {1}".format(text, regexp)

    def tearDown(self):
        super(SeleniumIDETest, self).tearDown()
        assert len(self.verificationErrors) == 0


class PageTest( FunctionalTest ) :
    """Тест определенной страницы. url задается через переменную url
    которая переопределяется в подклассах для разных страниц. Браузер с загруженной
    страницей доступен через self.webpage. Переменная класса status задает ожидаемый
    http-код страници. title, h1, title_xpath, h1_xpath - задают полоежение и ожидаемый
    контент тайтла и хедера страници"""

    url = u'www.lun.ua/'
    webpage = None
    status = 200

    title = None
    title_xpath = "/html/head/title"

    h1 = None
    h1_xpath = None

    subtests = None

    #text present merge
    texts_present = None

    #counter test merge
    texts_count = None

    def __init__(self) :
        super(PageTest, self).__init__()
        self.subtests = []

    def setUp(self):
        super(PageTest, self).setUp()

        if (not self.url.startswith( "http" )) :
            self.url = "http://" + self.url
        self.parsedUrl = urlparse( self.url )

        conn = httplib.HTTPConnection(self.parsedUrl.netloc)
        conn.request("HEAD", self.parsedUrl.path.encode('utf-8'))
        self.response = conn.getresponse()

        self.webpage = self.browser
        self.webpage.get( self.url )

    def run(self):
        super(PageTest, self).run()
        logger.write( u"url: {0}".format(html.link(self.url, self.url)) )

        ## check status code
        assert self.status == self.response.status, u"HTTP Response status expected {0}, recieved {1}".format(self.status, self.response.status)

        ## check title & header
        if not (self.title_xpath == None) and not (self.title == None) :
            assert_xpath_content( self.webpage, self.title_xpath, self.title )

        if not (self.h1_xpath == None) and not (self.h1 == None) :
            assert_xpath_content( self.webpage, self.h1_xpath, self.h1 )

        # text present merge
        if not self.texts_present is None :
            for ( xpath, text ) in self.texts_present :
                txt = self.webpage.find_element_by_xpath(xpath).text
                assert text in txt, u"Text '{0}' not found, present '{1}'".format(text, txt)

        # text count merge
        if not self.texts_count is None :
            for item in self.texts_count :
                count = self.webpage.page_source.count( item[0] )
                if item[1] == u'<' :
                    assert count < item[2],\
                    u"Text '{0}' occurs {1} times >= {2}".format( item[0], count, item[2] )
                if item[1] == u'=' :
                    assert count == item[2],\
                    u"Text '{0}' occurs {1} times != {2}".format( item[0], count, item[2] )
                if item[1] == u'>' :
                    assert count > item[2],\
                    u"Text '{0}' occurs {1} times <= {2}".format( item[0], count, item[2] )

                if item[1] == u'<=' :
                    assert count <= item[2],\
                    u"Text '{0}' occurs {1} times > {2}".format( item[0], count, item[2] )
                if item[1] == u'>=' :
                    assert count >= item[2],\
                    u"Text '{0}' occurs {1} times < {2}".format( item[0], count, item[2] )

        # execute sub tests
        for subtest in self.subtests :
            logger.write( u"Running test '{0}' of '{1}'".format( subtest.__doc__.decode("utf-8"), self.__doc__.decode("utf-8") ) )
            with logger.current_test( subtest ) :
                with browser.current_screenshot_dir( subtest.artifactsDir() ) :
                    try :
                        subtest.setUp( self.webpage )
                        subtest.run()
                        status = 'success'
                    except Exception as s :
                        status = 'fail'
                        logger.write( u"Error: {0}".format(s) )
                        snapshot()
                        raise SubTestFail( subtest.__doc__.decode("utf-8") )
                    finally:
                        subtest.tearDown()
                        logger.set_status( status )
                        logger.write( html.status_label( status ) )
                        logger.save_test_result()

    def tearDown(self):
        self.webpage = None
        super(PageTest, self).tearDown()

    def addSubtest(self, test):
        self.subtests.append( test )


class SubTest( Test ) :
    "тест может выполнятся только в контексте какого-то PageTest-а"

    webpage = None

    __parent_test__ = None

    def setUp( self, _webpage ) :
        super( SubTest, self ).setUp()
        self.webpage = _webpage

    def run(self) :
        pass

    def tearDown(self) :
        self.webpage = None
        super( SubTest, self ).tearDown()


class TypeaheadTest( SubTest ) :

    input_xpath = None
    ac_xpath = u"/html/body/div[@class='ac_results']"

    autocomplete = None

    def run(self) :
        if not (self.input_xpath is None) :
            elem = self.webpage.find_element_by_xpath(self.input_xpath)
            for x in self.autocomplete :
                elem.clear()
                elem.send_keys(x)
                time.sleep(3)
                ac = self.webpage.find_element_by_xpath(self.ac_xpath)
                for phrase in self.autocomplete[x] :
                    assert phrase in ac.text, u"Ошибка автокомплита: не найдено: {0} в автокомплите: {1}, предложенный автокомплит: {2}".format( phrase, x, ac.text )


class LoadOnSelectTest( SubTest ) :
    select_xpath = None
    loaded_element_xpath = None
    select = None

    def run(self):
        sel = Select(self.webpage.find_element_by_xpath( self.select_xpath ))
        for item in self.select :
            try :
                sel.select_by_visible_text( item[0] )
            except NoSuchElementException :
                assert False, u"В селекте (xpath='{0}') не найден пункт с текстом '{1}'".format( self.select_xpath, item[ 0 ] )

            time.sleep(2)
            text = self.webpage.find_element_by_xpath( self.loaded_element_xpath ).text
            for word in item[1] :
                assert word in text, u"При выборе '{0}' не подгрузилось поле '{1}', подгруженные элементы: '{2}'".format(item[0], word, text)


class SubTestFail( Exception ) :
    pass


## util functions
def click_all( ff, elems ) :
    if type(elems) == list :
        for elem in elems :
            try :
                ff.find_element_by_xpath( elem ).click()
            except :
                pass
    else :
        try :
            ff.find_element_by_xpath( elems ).click()
        except :
            pass


def assert_xpath_content(webpage, xpath, waited_content):
    real_content = webpage.find_element_by_xpath( xpath ).text
    assert real_content == waited_content, u"Comparing content on xpath {0}, expect: '{1}', recieved '{2}'".format( xpath, waited_content, real_content )

def url_unquote(url) :
    return urllib.unquote( url.encode('utf-8') ).decode('utf-8')

def test_name(test) :
    if (isinstance(test, Test)) :
        return test_name(test.__class__)
    elif (issubclass(test, MainTest)) :
        return test.__name__
    elif (issubclass(test, SubTest)) :
        return test.__parent_test__ + "_" + test.__name__
    else :
        return "not a test"

def to_unicode( s ) :
    if not isinstance( s, unicode ):
        return s.decode('utf-8')
    else :
        return s

def snapshot():
    img_url = browser.snapshot()
    logger.add_artifact({u"type":u"snapshot", u"path":img_url})


def element_present( ff, x ) :
    try :
        ff.by_x( x )
        res = True
    except :
        res = False
    return res


def merge( a, b, path=None ):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a
