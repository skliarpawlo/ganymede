from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime import models
from core import db
import json
from testing_runtime import tests_config
from testlib import utils

def gather_tests_info( selected_tests = [] ) :
    tests = []

    all_tests = tests_config.all_tests()
    for i in all_tests :
        pagetest = all_tests[i]()
        if isinstance(pagetest, utils.PageTest) :
            test = {}
            test[ 'id' ] = utils.test_id(pagetest)
            test[ 'url' ] = pagetest.url
            test[ 'doc' ] = pagetest.__doc__
            test[ 'checked' ] = utils.test_id(pagetest) in selected_tests
            test[ 'subtests' ] = []
            for j in all_tests :
                subtest = all_tests[j]()
                if isinstance(subtest, utils.SubTest) and\
                   subtest.__parent_test__ == i :
                    stest = {}
                    stest[ 'id' ] = utils.test_id(subtest)
                    stest[ 'doc' ] = subtest.__doc__
                    stest[ 'checked' ] = utils.test_id(subtest) in selected_tests
                    test[ 'subtests' ].append( stest )
            tests.append( test )
    return tests

def create_test(request) :
    if request.method == 'POST' :
        code = request.POST['code']
        test = models.StoredTest( code=code, status='NEW' )
        db.session.add( test )
        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/json")
    else :
        return render_to_response('test/create/create_test.html')

def list_tests(request) :
    stored_tests = gather_tests_info()
    return render_to_response('test/list/tests_list.html', { "tests" : stored_tests })

def update_test(request, test_id) :
    if request.method == "POST" :
        db.session\
        .query(models.StoredTest)\
        .filter( models.StoredTest.test_id == tests_config.test_id_to_db(test_id) )\
        .update( {
            "code" : request.POST['code'],
            "status" : request.POST['status']
        } )

        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/json")
    else :
        test_model = db.session\
        .query( models.StoredTest )\
        .filter( models.StoredTest.test_id == tests_config.test_id_to_db(test_id) )\
        .one()
        test = {}
        test["id"] = test_model.test_id
        test["name"] = test_id
        test["code"] = test_model.code
        test["status"] = test_model.status
        if issubclass(tests_config.all_tests()[ test_id ], utils.PageTest) :
            test["type"] = "pagetest"
        else :
            test["type"] = "subtest"
        return render_to_response("test/update/update_test.html",{"test":test})