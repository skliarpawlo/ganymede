from core import db
import json
from django.http import HttpResponse
import traceback

class DbMiddleware :
    def process_request(self, request):
        # init db
        db.init()

    def process_response(self, request, response):
        # release db session
        try :
            db.close()
        except :
            json_resp = json.dumps( { "status" : "error", "content" : traceback.format_exc() } )
            return HttpResponse(json_resp, mimetype="application/json")
        return response
