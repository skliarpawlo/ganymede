from django.conf.urls import patterns, include, url
from django.views.static import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^$', 'ganymede.views.home')
)
