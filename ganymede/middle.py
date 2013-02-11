from core import db

class DbMiddleware :
    def process_request(self, request):
        # init db
        db.init()

    def process_response(self, request, response):
        # release db session
        db.close()
        return response
