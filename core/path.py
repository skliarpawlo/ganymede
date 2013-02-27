import os
import shutil

def copy( _from_file, _to_dir ):
    shutil.copy( _from_file, _to_dir )

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
    if not os.path.exists( path ) :
        oldmask = os.umask(0000)
        os.makedirs(path,0777)
        os.umask(oldmask)

class cd:
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)