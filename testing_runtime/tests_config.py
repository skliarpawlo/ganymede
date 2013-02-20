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
