from core import db
import json
from django.http import HttpResponse
import traceback

class DbMiddleware :
    def process_request(self, request):
        # init db
        db.init()

    def process_response(self, request, response):
        try :
            db.session.commit()
        except :
            db.session.rollback()
            raise
        return response

    def process_exception(self, request, exception):
        db.session.rollback()
