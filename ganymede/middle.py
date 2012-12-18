from core import urls
from core import db
from core import mode

class GanymedeMiddleware :
    def process_request(self, request):
        # fix domain
        cur_domain = request.GET.get('domain')
        if (cur_domain is None) :
            cur_domain = "lun.ua"
        urls.domain = cur_domain

        # init db
        db.init()

        #set testing mode
        mode.set( mode.PRODUCTION )

    def process_response(self, request, response):
        # release db session
        db.close()
        return response