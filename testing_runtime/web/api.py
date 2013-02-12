from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
import sys

def call( request ) :
    try :
        pack = request.GET["package"]
        method = request.GET["method"]
        params = json.loads( request.GET["params"] )
        mod = __import__( pack, globals(), locals(), method, -1 )
        callable = getattr(mod, method)
        res = callable( *params )
    except :
        return HttpResponse( json.dumps( { "status" : "error", "content" : repr(sys.exc_info()[2].format_exception()) } ), mimetype="application/json" )
    return HttpResponse( json.dumps( { "status" : "ok", "content" : res } ), mimetype="application/json" )