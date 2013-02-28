from core import db
from django.http import HttpResponse

class DbMiddleware :

    def is_static(self, request):
        return request.path.startswith("/static/") or \
               request.path.startswith("/favicon.ico") or \
               request.path.startswith("/jsi18n")

    def process_request(self, request):
        if self.is_static( request ) :
            return

        # init db
        db.init()

    def process_response(self, request, response):
        if self.is_static( request ) :
            return response

        db.close()
        return response

    def process_exception(self, request, exception):
        if self.is_static( request ) :
            return

        db.close()
