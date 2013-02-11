from django.conf.urls import patterns, url, include
import settings

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),

    url(r'^$', 'ganymede.views.index'),

    url(r'^job/create$', 'testing_runtime.web.job.create_job'),
    url(r'^job/update$', 'testing_runtime.web.job.update_job'),
    url(r'^job/list$', 'testing_runtime.web.job.list_jobs'),
    url(r'^job/remove$', 'testing_runtime.web.job.remove_job'),

    url(r'^job/state$', 'testing_runtime.web.tasks.system_state'),
    url(r'^job/run$', 'testing_runtime.web.tasks.run_job'),
    url(r'^ajax/call$', 'testing_runtime.web.api.call'),

    url(r'^.*\.png', 'ganymede.views.screenshot'),
)
