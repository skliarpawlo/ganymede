# coding: utf-8

from core import browser
from core import vscreen
from core import path
from core import logger
from core import db
import os
import ganymede.settings
import httplib
from urlparse import urlparse
import urllib
from testing_runtime.web.decorators import html
import time
from selenium.webdriver.support.ui import Select

heap_dir = ganymede.settings.HEAP_PATH
base_dir = ganymede.settings.BASE_PATH

class Test( object ):

    def setUp(self):
        path.ensure( self.testDir() )
        db.reconnect()

    def tearDown(self):
        pass

    def testDir(self) :
        return os.path.join(heap_dir, "tests", test_name(self))

    def pidFile(self) :
        return os.path.join(heap_dir, "tests", test_name(self), "lock.pid")

class MainTest(Test) :

    def run(self):
        logger.write( u"Running test '{0}'".format(test_name(self)) )

    def snapshot(self):
        pass

class RedirectTest(MainTest) :

    # [ [ url, redirect_status, to_url, to_status ],... ]
    redirects = []

    def run(self):
        super(RedirectTest, self).run()

        for (from_url, redirect_status, dest_url, dest_status) in self.redirects :
            logger.write( u"Редирект: {0}({1}) -> {2}({3})".\
            format(html.link(from_url,from_url), str(redirect_status),
                html.link(dest_url,dest_url), str(dest_status) ))

            parsed_url = urlparse( from_url )
            conn = httplib.HTTPConnection( parsed_url.netloc )
            conn.request( "HEAD", parsed_url.path.encode('utf-8') )
            from_response = conn.getresponse()

            assert from_response.status == redirect_status, \
            u"Статус редиректа не правильный ({0}), ожидался {1}".\
            format(from_response.status, redirect_status)

            loc = from_response.getheader('location')

            assert loc == dest_url, \
            u"Редиректит не туда {0}, ожидалось {1}".\
            format(loc, dest_url)

            parsed_url2 = urlparse( loc )
            conn2 = httplib.HTTPConnection( parsed_url2.netloc )
            conn2.request( "HEAD", parsed_url2.path.encode('utf-8') )
            dest_response = conn2.getresponse()

            assert dest_response.status == dest_status, \
            u"Статус страницы назначения не правильный ({0}), ожидался {1}".\
            format(from_response.status, redirect_status)

class FunctionalTest(MainTest) :

    browser = None

    def setUp(self):
        super(FunctionalTest, self).setUp()

        path.clean( self.photosDir() )

        # ensure paths
        path.ensure( self.photosDir() )

        # functional tests setup
        vscreen.start()
        browser.start()
        browser.setHeap(self.photosDir())
        self.browser = browser.inst

    def tearDown(self):
        self.browser = None

        browser.stop()
        vscreen.stop()

        super(FunctionalTest, self).tearDown()

    def photosDir(self):
        return os.path.join(self.testDir(), "photos")

    def snapshot(self):
        img_url = browser.snapshot()
        logger.add_artifact({u"type":u"snapshot", u"source":test_name(self), u"path":img_url})

class PageTest( FunctionalTest ) :
    """Тест определенной страницы. url задается через переменную url
    которая переопределяется в подклассах для разных страниц. Браузер с загруженной
    страницей доступен через self.webpage. Переменная класса status задает ожидаемы
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

        # execute sub tests
        for subtest in self.subtests :
            logger.write( u"Running subtest '{0}' of '{1}'".format(test_name(subtest),test_name(self)) )
            subtest.setUp( self.webpage )
            subtest.run()
            subtest.tearDown()

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
                    assert phrase in ac.text, u"Ошибка автокомплита: не найдено {0} в автокомплите {1}".format( phrase, ac.text )

class CounterTest( SubTest ) :
    texts = None

    def run(self):
        for item in self.texts :
            count = self.webpage.page_source.count( item[0] )
            if item[1] == u'<' :
                assert count < item[2], \
                u"Текст '{0}' встречается {1} раз, это не меньше чем {2}".format( item[0], count, item[2] )
            if item[1] == u'=' :
                assert count == item[2],\
                u"Текст '{0}' встречается {1} раз, это не равно {2}".format( item[0], count, item[2] )
            if item[1] == u'>' :
                assert count > item[2],\
                u"Текст '{0}' встречается {1} раз, это не больше чем {2}".format( item[0], count, item[2] )

            if item[1] == u'<=' :
                assert count <= item[2],\
                u"Текст '{0}' встречается {1} раз, это бальше чем {2}".format( item[0], count, item[2] )
            if item[1] == u'>=' :
                assert count >= item[2],\
                u"Текст '{0}' встречается {1} раз, это меньше чем {2}".format( item[0], count, item[2] )

class LoadOnSelectTest( SubTest ) :
    select_xpath = None
    loaded_element_xpath = None
    select = None

    def run(self):
        sel = Select(self.webpage.find_element_by_xpath( self.select_xpath ))
        for item in self.select :
            sel.select_by_visible_text( item[0] )
            time.sleep(2)
            text = self.webpage.find_element_by_xpath( self.loaded_element_xpath ).text
            for word in item[1] :
                assert word in text, u"При выборе '{0}' не подгрузилось поле '{1}', подгруженные элементы: '{2}'".format(item[0], word, text)

class TextPresent( SubTest ) :
    text = None
    text_xpath = "/html/body"

    def run(self):
        if not self.text is None :
            txt = self.webpage.find_element_by_xpath(self.text_xpath).text
            assert self.text in txt, u"Нету текста '{0}', найден текст '{1}'".format(self.text, txt)

## util functions
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
