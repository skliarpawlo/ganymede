import inspect
from testlib import utils
from core import db
from sqlalchemy import func
from testing_runtime import models

_all_tests = None
_test_id_to_status = None
_test_id_to_whose = None

def test_id_to_status( test_id ) :
    global _test_id_to_status
    if _test_id_to_status is None :
        _fetch_tests()
    return _test_id_to_status[ test_id ]

def test_id_to_whose( test_id ) :
    global _test_id_to_whose
    if _test_id_to_whose is None :
        _fetch_tests()
    return _test_id_to_whose[ test_id ]

def all_tests() :
    global _all_tests
    if _all_tests is None :
        _fetch_tests()
    tests_count = db.session.query( func.count( models.StoredTest.test_id ) ).scalar()
    if len( _all_tests ) != tests_count :
        _fetch_tests()
    return _all_tests

def test_to_id( test ) :
    class_name = utils.test_name(test)
    all_t = all_tests()
    for x in all_t :
        if utils.test_name(all_t[x]) == class_name :
            return x

def _fetch_tests() :
    global _all_tests, _test_id_to_status, _test_id_to_whose

    _all_tests = {}
    _test_id_to_status = {}
    _test_id_to_whose = {}

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
                if inspect.isclass(test) and issubclass(test, utils.Test) :
                    _all_tests[ stored_test.test_id ] = test
                    _test_id_to_status[ stored_test.test_id ] = stored_test.status
                    _test_id_to_whose[ stored_test.test_id ] = stored_test.whose
