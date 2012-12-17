from core import db
from core import browser
from core import vscreen
from core import path
from core import urls
import os
import ganymede.settings


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

        # functional tests setup
        db.init()
        vscreen.start()
        browser.start()
        browser.setHeap(self.photo_dir)

    def tearDown(self):
        browser.stop()
        vscreen.stop()
        db.close()

def test_dir(test_id) :
    return os.path.join(heap_dir, "tests", test_id)

def photos_dir(test_id) :
    return os.path.join(test_dir(test_id), "photos")

def pid_file(test_id) :
    return os.path.join(heap_dir, "tests", test_id, urls.domain + ".pid")
