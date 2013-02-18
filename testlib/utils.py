# coding: utf-8

from core import browser
from core import vscreen
from core import path
from core import logger
import os
import ganymede.settings
import httplib
from urlparse import urlparse
import urllib

heap_dir = ganymede.settings.HEAP_PATH
base_dir = ganymede.settings.BASE_PATH

class Test( object ):

    def setUp(self):
        path.ensure( self.testDir() )

    def tearDown(self):
        pass

    def testDir(self) :
        return os.path.join(heap_dir, "tests", test_id(self))

    def pidFile(self) :
        return os.path.join(heap_dir, "tests", test_id(self), "lock.pid")

class FunctionalTest(Test) :

    def setUp(self):
        super(FunctionalTest, self).setUp()

        path.clean( self.photosDir() )

        # ensure paths
        path.ensure( self.photosDir() )

        # functional tests setup
        vscreen.start()
        browser.start()
        browser.setHeap(self.photosDir())

    def tearDown(self):
        browser.stop()
        vscreen.stop()

        super(FunctionalTest, self).tearDown()

    def photosDir(self):
        return os.path.join(self.testDir(), "photos")

    def snapshot(self):
        img_url = browser.snapshot()
        logger.add_artifact({u"type":u"snapshot", u"source":test_id(self), u"path":img_url})

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

        self.webpage = browser.inst
        self.webpage.get( self.url )

    def run(self):
        ## check status code
        assert self.status == self.response.status

        ## check title & header
        if not (self.title_xpath == None) and not (self.title == None) :
            assert_xpath_content( self.webpage, self.title_xpath, self.title )

        if not (self.h1_xpath == None) and not (self.h1 == None) :
            assert_xpath_content( self.webpage, self.h1_xpath, self.h1 )

        # execute sub tests
        for subtest in self.subtests :
            logger.write( u"Running subtest '{0}' of '{1}'".format(test_id(subtest),test_id(self)) )
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

## util functions
def assert_xpath_content(webpage, xpath, waited_content):
    real_content = webpage.find_element_by_xpath( xpath ).text
    assert real_content == waited_content, u"Comparing content on xpath {0}, expect: '{1}', recieved '{2}'".format( xpath, waited_content, real_content )

def url_unquote(url) :
    return urllib.unquote( url.encode('utf-8') ).decode('utf-8')

def test_id(test) :
    if (isinstance(test, Test)) :
        return test_id(test.__class__)
    elif (issubclass(test, PageTest)) :
        return test.__name__
    elif (issubclass(test, SubTest)) :
        return test.__parent_test__ + "_" + test.__name__
    else :
        return "not a test"
