# coding: utf-8

from decorators import html
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext as _
from testing_runtime import models
import json
from core import db
import traceback


def verify_module(module_id=None,code=None) :
    errors = []
    try :
        dc = {}
        exec code in dc
    except :
        errors.append( u'exec модуля рыгнул exception: {0}'.format(traceback.format_exc().decode('utf-8')) )
    return errors


def gather_modules_info() :
    res = []

    all = db.session.query( models.Module ).all()

    for m in all :
        res.append( {
            "module_id" : m.module_id,
            "name" : m.name,
            "path" : m.path
        } )

    return res


def list_modules( request ) :
    title = html.title( [ _('Modules'), 'Ganymede' ] )
    modules = gather_modules_info()
    return render_to_response(
        'modules/list.html',
        { "modules" : modules, 'title' : title },
        context_instance=RequestContext(request)
    )


def add_module(request) :

    title = html.title( [ _('Add module'), _('Modules'), 'Ganymede' ] )

    if request.method == 'POST' :
        err = verify_module( module_id=None, code=request.POST['code'] )
        if len(err) == 0 :
            name = request.POST['name']
            code = request.POST['code']
            path = request.POST['path']
            test = models.Module( name=name, path=path, code=code )
            db.session.add( test )
            json_resp = json.dumps( { "status" : "ok" } )
            return HttpResponse(json_resp, mimetype="application/json")
        else :
            json_resp = json.dumps( { "status" : "error", "content" : err } )
            return HttpResponse(json_resp, mimetype="application/json")
    else :
        return render_to_response(
            'modules/add.html',
            { 'title' : title },
            context_instance=RequestContext(request)
        )


def update_module(request, module_id) :

    title = html.title( [ _('Update module'), _('Modules'), 'Ganymede' ] )
    module = db.session.query( models.Module ).get( module_id )

    if request.method == 'POST' :
        err = verify_module( module_id=None, code=request.POST['code'] )
        if len(err) == 0 :
            module.name = request.POST['name']
            module.code = request.POST['code']
            module.path = request.POST['path']

            json_resp = json.dumps( { "status" : "ok" } )
            return HttpResponse(json_resp, mimetype="application/json")
        else :
            json_resp = json.dumps( { "status" : "error", "content" : err } )
            return HttpResponse(json_resp, mimetype="application/json")
    else :
        return render_to_response(
            'modules/update.html',
            { 'title' : title, 'module' : module },
            context_instance=RequestContext(request)
        )

def remove_module(request) :
    if request.method == 'POST' :
        module = db.session.query( models.Module ).get( int(request.POST[ "module_id" ]) )
        db.session.delete( module )

        json_resp = json.dumps( { "status" : "ok" } )
        return HttpResponse(json_resp, mimetype="application/json")

