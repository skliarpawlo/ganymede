#import imp
#import glob
#import os
import inspect
from testlib import utils
from core import db
from testing_runtime import models

_all_tests = None
_test_id_to_db = None
_test_id_to_status = None

def test_id_to_status( test_id ) :
    global _test_id_to_status
    if _test_id_to_status is None :
        _fetch_tests()
    return _test_id_to_status[ test_id ]


def test_id_to_db( test_id ) :
    global _test_id_to_db
    if _test_id_to_db is None :
        _fetch_tests()
    return _test_id_to_db[ test_id ]

def all_tests() :
    global _all_tests, _test_id_to_db
    if _all_tests is None :
        _fetch_tests()
    return _all_tests

def _fetch_tests() :
    global _all_tests, _test_id_to_db, _test_id_to_status

    _all_tests = {}
    _test_id_to_db = {}
    _test_id_to_status = {}

    #######################################
    # search for tests ing tests_root dir #
    #######################################
    #for test_path in glob.glob( os.path.join(os.path.dirname(__file__), "../", "tests_root/**/*.py") ):
    #    if test_path[-11:] == "__init__.py":
    #        continue
    #    try:
    #        mod_name = ".".join( test_path.split("tests_root")[-1].split("/") )[1:-3]
    #        mod = imp.load_source( mod_name, test_path )
    #        for name, obj in inspect.getmembers( mod ) :
    #            if (inspect.isclass(obj)) and (obj.__module__ == mod_name) and \
    #               issubclass(obj, (utils.PageTest,utils.SubTest)) :
    #                _all_tests[ utils.test_id(obj) ] = obj
    #
    #    except ImportError, m :
    #        print "Error while importing %s - %s"%(test_path,m)

    #####################
    #fetch tests from db#
    #####################
    for stored_test in db.session.query( models.StoredTest ).all() :
        code = stored_test.code

        #remember locals
        b = locals().keys()

        #execute test code
        exec code

        #checkout wich name appeared in locals
        a = locals().keys()
        for x in a :
            if not x in b :
                test = locals()[x]
                if inspect.isclass(test) and issubclass(test, (utils.PageTest,utils.SubTest)) :
                    _all_tests[ utils.test_id(test) ] = test
                    _test_id_to_db[ utils.test_id(test) ] = stored_test.test_id
                    _test_id_to_status[ utils.test_id(test) ] = stored_test.status
