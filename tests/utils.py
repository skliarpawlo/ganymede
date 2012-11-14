import core.path
import core.lock
from core import db
from core import browser
from core import vscreen
import core.process
import os
import sys
import codecs
import logging
import unittest
from cStringIO import StringIO
import shutil
import ganymede.settings

heap_dir = ganymede.settings.HEAP_PATH
base_dir = ganymede.settings.BASE_PATH

class FunctionalTest(unittest.TestCase) :
    def setUp(self):
        # set paths
        self.test_dir = test_dir( self.id )
        self.pid_file = pid_file( self.id )
        self.log_file = log_file( self.id )
        self.photo_dir = photos_dir( self.id )

#        stdio redirect to string
#        sys.stderr = sys.stdout = StringIO()
#        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#        sys.stderr = codecs.getwriter('utf8')(sys.stderr)

        try :
            for root, dirs, files in os.walk(self.photo_dir):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        except :
            pass

        # ensure paths
        try :
            os.makedirs( self.test_dir )
        except os.error :
            pass
        try :
            os.makedirs( self.photo_dir )
        except os.error :
            pass

        # logging config
        logging.basicConfig(filename=self.log_file, level=logging.INFO, filemode='w', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        self.logger = logging.getLogger(self.id)

        # functional tests setup
        db.init()
        vscreen.start()
        browser.start()
        browser.setHeap(self.photo_dir)

    def tearDown(self):
        # save test out to log
#        self.logger.info(sys.stdout.getvalue())

#        sys.stdout.close()
#        sys.stderr.close()

        browser.stop()
        vscreen.stop()
        db.session.close()


class LockException(Exception) :
    def __init__(self, msg):
        self.msg = msg

def run_test(test_id):
    fpid = pid_file(test_id)
    stu_pid=core.lock.is_free(fpid)
    if stu_pid==0:
        core.process.daemonize()
        core.lock.capture(fpid)
        try :
            unittest.main(module='tests.' + test_id + '.test_' + test_id)
        finally :
            core.lock.uncapture(fpid)
    else :
        raise Exception('Lock failed. PID=' + stu_pid)

def dump_log(test_id):
    "Show log content"
    f = open(log_file(test_id), "r")
    log = f.read()
    f.close()
    return log

def test_dir(test_id) :
    return os.path.join(heap_dir, "tests", test_id)

def pid_file(test_id) :
    return os.path.join(test_dir(test_id), ".pid")

def log_file(test_id) :
    return os.path.join(test_dir(test_id), ".log")

def photos_dir(test_id) :
    return os.path.join(test_dir(test_id), "photos")

if (__name__=='__main__'):
    run_test('check_redirects')