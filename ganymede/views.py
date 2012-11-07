def home(request) :
    from django.shortcuts import render_to_response

    return render_to_response( 'all_tests.html', {
        'tests' : ( 'seo_texts', )
    } )

def test(request) :
    from django.http import HttpResponse
    import json

    test_id = request.GET.get('test_id')
    op_id = request.GET.get('op_id')
    return HttpResponse( json.dumps( {
        'test_id' : test_id,
        'op_id' : op_id
    } ), mimetype='application/json' )

