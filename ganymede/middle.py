from core import db
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import urllib
from testing_runtime.models import User
from sqlalchemy import func
import datetime
from django.core.urlresolvers import resolve


def is_static(request):
    return request.path.startswith("/static/") or\
           request.path.startswith("/favicon.ico") or\
           request.path.startswith("/jsi18n") or\
           request.path.startswith("/i18n")

class DbMiddleware :

    def process_request(self, request):
        if is_static( request ) :
            return

        # init db
        db.init()

    def process_response(self, request, response):
        if is_static( request ) :
            return response

        db.close()
        return response


class UserAuthMiddleware :

    def process_request(self, request):
        if is_static( request ) :
            return

        id_cookie = request.COOKIES['gany_user_identity'] if 'gany_user_identity' in request.COOKIES else '-'
        user = db.user_session.query( User ).filter( func.md5( User.salt ) == id_cookie ).first()

        if not request.path.startswith("/user/login") and \
           user is None :
            return redirect( u"{login_url}?{next_url}".format(
                login_url = reverse( "testing_runtime.web.user.login_page" ),
                next_url = urllib.urlencode( {"next" : request.path } )
            ) )

        request.user = user

    def process_response(self, request, response):
        return response


class ViewNameMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if is_static( request ) :
            return
        request.view = resolve(request.path).url_name