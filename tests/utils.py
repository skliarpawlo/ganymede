import core.path
from core import db
from core import browser
from core import vscreen
import os
import unittest
import shutil
import ganymede.settings

heap_dir = ganymede.settings.HEAP_PATH
base_dir = ganymede.settings.BASE_PATH

class FunctionalTest(unittest.TestCase) :
    def setUp(self):
        # set paths
        self.test_dir = test_dir( self.id )
        self.photo_dir = photos_dir( self.id )

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

        # functional tests setup
        db.init()
        vscreen.start()
        browser.start()
        browser.setHeap(self.photo_dir)

    def tearDown(self):
        browser.stop()
        vscreen.stop()
        db.session.close()

def test_dir(test_id) :
    return os.path.join(heap_dir, "tests", test_id)

def photos_dir(test_id) :
    return os.path.join(test_dir(test_id), "photos")
