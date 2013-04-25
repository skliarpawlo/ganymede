# coding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect
from testing_runtime.models import User
from core import db
from testing_runtime.forms import LoginForm
import hashlib
from django.template import RequestContext


def login_page( request ) :
    form = LoginForm( request.POST )
    if request.method == 'POST' and form.validate() :
        user = db.user_session.query( User ).filter( User.username == request.POST["username"] ).first()
        if user.validate_password( request.POST['password'] ) :
            resp = redirect( request.GET[ 'next' ] if 'next' in request.GET else '/' )
            resp.set_cookie( User.COOKIE_KEY, user.cookie_hash() )
            return resp

    return render_to_response(
        'user/login_page.html',
        { "form" : form },
        context_instance=RequestContext(request)
    )


def logout( request ) :
    resp = redirect( request.GET[ 'next' ] if 'next' in request.GET else '/' )
    resp.set_cookie( User.COOKIE_KEY, "" )
    return resp
