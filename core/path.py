import os
import shutil

def clean( dir ):
    try :
        for root, dirs, files in os.walk(dir):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    except :
        pass

def ensure( path ):
    try :
        os.makedirs( path )
    except os.error :
        pass
