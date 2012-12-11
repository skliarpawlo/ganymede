from core import db
from core import browser
from core import vscreen
from core import path
import os
import sys
import ganymede.settings
import codecs
from cStringIO import StringIO

heap_dir = ganymede.settings.HEAP_PATH
base_dir = ganymede.settings.BASE_PATH

class FunctionalTest :
    def __init__(self, test_id):
        self.id = test_id

    def setUp(self):
        # set paths
        self.test_dir = test_dir( self.id )
        self.photo_dir = photos_dir( self.id )

        path.clean( self.photo_dir )

        # ensure paths
        path.ensure( self.test_dir )
        path.ensure( self.photo_dir )

        # redirect to log
        # if not ganymede.settings.DEBUG:
        self._err = sys.stderr
        self._out = sys.stdout
        sys.stderr = sys.stdout = StringIO()
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        sys.stderr = codecs.getwriter('utf8')(sys.stderr)

        # functional tests setup
        db.init()
        vscreen.start()
        browser.start()
        browser.setHeap(self.photo_dir)

    def tearDown(self):
        browser.stop()
        vscreen.stop()
        db.session.close()

        # if not ganymede.settings.DEBUG:
        log = sys.stdout.getvalue()
        fd = open( log_file(self.id), 'w' )
        fd.write(log)
        fd.close()

        sys.stdout.close()
        sys.stderr.close()

        sys.stdout = self._out
        sys.stderr = self._err

def test_dir(test_id) :
    return os.path.join(heap_dir, "tests", test_id)

def photos_dir(test_id) :
    return os.path.join(test_dir(test_id), "photos")

def log_file(test_id) :
    return os.path.join(heap_dir, "tests", test_id, ".log")

def pid_file(test_id) :
    return os.path.join(heap_dir, "tests", test_id, ".pid")

def res_file(test_id) :
    return os.path.join(heap_dir, "tests", test_id, ".res")

def dump_log(test_id):
    try:
        f = open(log_file(test_id), "r")
        log = f.read()
        f.close()
    except IOError :
        log = "no log available"
    return log

def dump_res(test_id):
    try:
        f = open(res_file(test_id), "r")
        log = f.read()
        f.close()
    except IOError :
        log = "no result"
    return log
