def home(request) :
    from django.shortcuts import render_to_response

    return render_to_response( 'all_tests.html', {
        'tests' : ( 'seo_texts', )
    } )

def test(request) :
    from django.http import HttpResponse
    import json
    import tests.utils

    test_id = request.GET.get('test_id')
    op_id = request.GET.get('op_id')

    test = tests.utils.get_test_by_id( test_id )

    return HttpResponse( json.dumps( {
        'test_id' : test_id,
        'op_id' : op_id
    } ), mimetype='application/json' )

