import tests_root.general.status
import tests_root.seo.texts
import tests_root.seo.titles
import imp
import os, glob, inspect
import utils
from core import mode

all_tests = {}

for test_path in glob.glob("tests/tests_root/" + mode.testcase + "/*.py"):
    if test_path[-11:] == "__init__.py":
        continue
    try:
        mod_name = ".".join( test_path.split("/") )[:-3]
        mod = imp.load_source( mod_name, test_path )
        for name, obj in inspect.getmembers( mod ) :
            if (inspect.isclass(obj)) and (obj.__module__ == mod_name) and issubclass(obj, utils.FunctionalTest) :
                all_tests[ mod_name.split(".")[-1] ] = obj
    except ImportError, m :
        print "Error while importing %s - %s"%(test_path,m)
