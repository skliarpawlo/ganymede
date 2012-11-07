from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^$', 'ganymede.views.home'),
    url(r'^ajax/test$', 'ganymede.views.test'),
)
