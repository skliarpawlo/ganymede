import core.path
import core.lock
import os
import imp
import sys
import codecs
import logging
from cStringIO import StringIO

class Test :
    def __init__(self, id):
        self.id = id
        self.test_dir = core.path.test_dir( id )
        self.pid_file = os.path.join( self.test_dir, ".pid" )
        self.log_file = os.path.join( self.test_dir, ".log" )
        self.photo_dir = core.path.photos_dir( id )
        self.test_exe = core.path.test_exe( id )
        try :
            os.makedirs( self.test_dir )
        except os.error :
            pass
        try :
            os.makedirs( self.photo_dir )
        except os.error :
            pass

    def log(self):
        f = open(self.log_file, "r")
        log = f.read()
        f.close()
        return log

    def execute(self) :
        success = core.lock.capture(self.pid_file)
        if (success == core.lock.STATUS_SUCCESS) :
            try :
                sys.stderr = sys.stdout = StringIO()
                sys.stdout = codecs.getwriter('utf8')(sys.stdout)
                sys.stderr = codecs.getwriter('utf8')(sys.stderr)

                logging.basicConfig(filename=self.log_file, level=logging.INFO, filemode='w', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
                logger = logging.getLogger(self.id)

                imp.load_source(self.id, self.test_exe)

                logger.info(sys.stdout.getvalue())

                sys.stdout.close()
                sys.stderr.close()
            finally :
                core.lock.uncapture(self.pid_file)
        else :
            raise Exception('Lock failed')


def get_test_by_id(test_id) :
    return Test(test_id)

if (__name__ == '__main__') :
    test = get_test_by_id('seo_texts')
    test.execute()
