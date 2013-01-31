from django.conf.urls import patterns, url, include
import settings

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
        }),

    url(r'^$', 'ganymede.views.index'),

    url(r'^job/state$', 'ganymede.views.system_state'),
    url(r'^job/create$', 'ganymede.views.create_job'),
    url(r'^job/list$', 'ganymede.views.list_jobs'),

    url(r'^tests/create$', 'ganymede.views.create_test'),
    url(r'^tests/list$', 'ganymede.views.list_tests'),


    url(r'^ajax/test$', 'ganymede.views.test'),
    url(r'^.*\.png', 'ganymede.views.screenshot'),
)
