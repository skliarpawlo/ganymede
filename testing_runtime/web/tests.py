# coding: utf-8

import ganymede.settings
from django.shortcuts import render_to_response
from django.http import HttpResponse
from testing_runtime import models
from core import db
import json
from testing_runtime import tests_config
from testlib import utils
import inspect
import traceback

def verify_test(test_id=None,code=None) :
    errors = []
    present = False
    try :
        #remember locals
        b = locals().keys()

        #execute test code
        exec code

        #checkout wich name appeared in locals
        all_tests = tests_config.all_tests()
        a = locals().keys()
        for x in a :
            if not x in b :
                test = locals()[x]
                if inspect.isclass(test) and issubclass(test, (utils.PageTest,utils.SubTest)) :
                    present = True

                    if issubclass(test, utils.SubTest) :
                        if test.__parent_test__ is None :
                            errors.append( u"Не указан аттрибут __parent_test__ у подтеста" )
                        else :
                            parent_here = False
                            for x in all_tests :
                                if utils.test_name(all_tests[x]) == test.__parent_test__ :
                                    parent_here = True
                            if not parent_here :
                                errors.append( u'Нету теста страницы с id="{0}"'.format(test.__parent_test__) )

                        if  not test.__parent_test__ is None :
                            all_tests = tests_config.all_tests()
                            class_name = utils.test_name(test)
                            for x in all_tests :
                                if not (test_id == x) and (utils.test_name(all_tests[x]) == class_name) :
                                    errors.append( u'Уже есть тест "{0}"'.format(utils.test_name(test)) )

    except :
        errors.append( u'exec теста рыгнул exception: {0}'.format(traceback.format_exc().decode('utf-8')) )

    if not present :
        errors.append( u'В коде не обнаружен класс теста' )

    return errors

def gather_tests_info( selected_tests = [] ) :
    tests_config._fetch_tests()

    tests = []

    all_tests = tests_config.all_tests()
    for i in all_tests :
        pagetest = all_tests[i]()
        if isinstance(pagetest, utils.PageTest) :
            test = {}
            test[ 'id' ] = i
            test[ 'name' ] = utils.test_name(pagetest)
            test[ 'url' ] = pagetest.url
            test[ 'doc' ] = pagetest.__doc__
            test[ 'checked' ] = i in selected_tests
            test[ 'subtests' ] = []
            test[ 'status' ] = tests_config.test_id_to_status( i )
            for j in all_tests :
                subtest = all_tests[j]()
                if isinstance(subtest, utils.SubTest) and\
                   subtest.__parent_test__ == utils.test_name(pagetest) :
                    stest = {}
                    stest[ 'id' ] = j
                    stest[ 'name' ] = utils.test_name(subtest)
                    stest[ 'doc' ] = subtest.__doc__
                    stest[ 'checked' ] = j in selected_tests
                    stest[ 'status' ] = tests_config.test_id_to_status( j )
                    test[ 'subtests' ].append( stest )
            tests.append( test )
    return tests

def create_test(request) :
    if request.method == 'POST' :
        err = verify_test( test_id=None, code=request.POST['code'] )
        if len(err) == 0 :
            code = request.POST['code']
            test = models.StoredTest( code=code, status='new' )
            db.session.add( test )
            json_resp = json.dumps( { "status" : "ok" } )
            return HttpResponse(json_resp, mimetype="application/json")
        else :
            json_resp = json.dumps( { "status" : "error", "content" : err } )
            return HttpResponse(json_resp, mimetype="application/json")
    else :
        return render_to_response('test/create/create_test.html')

def list_tests(request) :
    stored_tests = gather_tests_info()
    return render_to_response('test/list/tests_list.html', { "tests" : stored_tests })

def update_test(request, test_id) :
    test_id = int(test_id)
    if request.method == "POST" :
        err = verify_test( test_id = test_id, code = request.POST['code'] )
        if len(err) == 0 :
            db.session\
            .query(models.StoredTest)\
            .filter( models.StoredTest.test_id == test_id )\
            .update( {
                "code" : request.POST['code'],
                "status" : request.POST['status']
            } )

            json_resp = json.dumps( { "status" : "ok" } )
            return HttpResponse(json_resp, mimetype="application/json")
        else :
            json_resp = json.dumps( { "status" : "error", "content" : err } )
            return HttpResponse(json_resp, mimetype="application/json")

    else :
        test_model = db.session\
        .query( models.StoredTest )\
        .filter( models.StoredTest.test_id == test_id )\
        .one()
        test = {}
        test["id"] = test_id
        test["name"] = utils.test_name(tests_config.all_tests()[test_id])
        test["code"] = test_model.code
        test["status"] = test_model.status
        if issubclass(tests_config.all_tests()[ test_id ], utils.PageTest) :
            test["type"] = "pagetest"
        else :
            test["type"] = "subtest"
        return render_to_response("test/update/update_test.html",{"test":test})

def remove_test(request) :
    test_id = request.POST[ 'test_id' ]

    db.session.query(models.StoredTest).\
    filter(models.StoredTest.test_id == test_id).\
    delete()

    json_resp = json.dumps( { "status" : "ok" } )
    return HttpResponse(json_resp, mimetype="application/json")

def screenshot(request) :
    try :
        fd = open( ganymede.settings.HEAP_PATH + request.path )
        resp = HttpResponse( mimetype='image/png' )
        resp.write( fd.read() )
        fd.close()
        return resp
    except :
        return HttpResponse( content="file {0} not found".format(ganymede.settings.HEAP_PATH + request.path), mimetype='text/plain' )

def index(request) :
    return render_to_response( 'index.html' )
