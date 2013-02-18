from django.conf.urls import patterns, url, include
import settings

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),

    url(r'^$', 'testing_runtime.web.tests.index'),

    url(r'^job/create$', 'testing_runtime.web.job.create_job'),
    url(r'^job/update/(?P<job_name>\w+)$', 'testing_runtime.web.job.update_job'),
    url(r'^job/list$', 'testing_runtime.web.job.list_jobs'),
    url(r'^job/remove$', 'testing_runtime.web.job.remove_job'),

    url(r'^job/state$', 'testing_runtime.web.tasks.system_state'),
    url(r'^job/run$', 'testing_runtime.web.tasks.run_job'),

    url(r'^test/create$', 'testing_runtime.web.tests.create_test'),
    url(r'^test/list$', 'testing_runtime.web.tests.list_tests'),
    url(r'^test/update/(?P<test_id>\w+)$', 'testing_runtime.web.tests.update_test'),
    url(r'^.*\.png', 'testing_runtime.web.tests.screenshot'),

    url(r'^task/log/(?P<task_id>\w+)$', 'testing_runtime.web.tasks.log'),
    url(r'^ajax/call$', 'testing_runtime.web.api.call'),

)
