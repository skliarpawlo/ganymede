import core.path
import core.lock
from core import db
from core import browser
from core import vscreen
import os
import sys
import codecs
import logging
import unittest
from cStringIO import StringIO
import shutil

class FunctionalTest(unittest.TestCase) :
    def setUp(self):
        # set paths
        self.test_dir = core.path.test_dir( self.id )
        self.pid_file = os.path.join( self.test_dir, ".pid" )
        self.log_file = os.path.join( self.test_dir, ".log" )
        self.photo_dir = core.path.photos_dir( self.id )
        self.test_exe = core.path.test_exe( self.id )

        # stdio redirect to string
        sys.stderr = sys.stdout = StringIO()
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        sys.stderr = codecs.getwriter('utf8')(sys.stderr)

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

    def log(self):
        "Show log content"
        f = open(self.log_file, "r")
        log = f.read()
        f.close()
        return log

    def tearDown(self):
        # save test out to log
        self.logger.info(sys.stdout.getvalue())

        sys.stdout.close()
        sys.stderr.close()

        browser.stop()
        vscreen.stop()
        db.session.close()


class TestRunner :
    pass
#    # for subprocesses, etc
#    success = core.lock.capture(self.pid_file)
#    if (success == core.lock.STATUS_SUCCESS) :
#        try :
#        finally :
#            core.lock.uncapture(self.pid_file)
#        else :
#            raise Exception('Lock failed')
