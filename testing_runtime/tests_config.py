import imp
import glob, inspect
from testlib import utils
import os

all_tests = {}

# search for tests ing tests_root dir
for test_path in glob.glob( os.path.join(os.path.dirname(__file__), "../", "tests_root/**/*.py") ):
    if test_path[-11:] == "__init__.py":
        continue
    try:
        mod_name = ".".join( test_path.split("tests_root")[-1].split("/") )[1:-3]
        mod = imp.load_source( mod_name, test_path )
        for name, obj in inspect.getmembers( mod ) :
            if (inspect.isclass(obj)) and (obj.__module__ == mod_name) and \
               (issubclass(obj, utils.PageTest) or issubclass(obj, utils.SubTest)) :
                all_tests[ utils.test_id(obj) ] = obj

    except ImportError, m :
        print "Error while importing %s - %s"%(test_path,m)

#
#TODO: search for tests in db
#