from django.conf.urls import patterns, url, include

js_info_dict = {
    'domain': 'django',
    'packages': ('testing_runtime.web', ),
}

urlpatterns = patterns('',
    url(r'^$', 'testing_runtime.web.tests.index'),

    url(r'^job/add$', 'testing_runtime.web.job.add_job'),
    url(r'^job/update/(?P<job_id>\w+)$', 'testing_runtime.web.job.update_job'),
    url(r'^job/list$', 'testing_runtime.web.job.list_jobs'),
    url(r'^job/remove$', 'testing_runtime.web.job.remove_job'),

    url(r'^job/state$', 'testing_runtime.web.tasks.system_state'),
    url(r'^job/run$', 'testing_runtime.web.tasks.run_job'),

    url(r'^test/add$', 'testing_runtime.web.tests.add_test'),
    url(r'^test/list$', 'testing_runtime.web.tests.list_tests'),
    url(r'^test/update/(?P<test_id>\w+)$', 'testing_runtime.web.tests.update_test'),
    url(r'^test/remove$', 'testing_runtime.web.tests.remove_test'),
    url(r'^tags/typeahead$', 'testing_runtime.web.tests.tags_typeahead'),
    url(r'^.*\.png$', 'testing_runtime.web.tests.screenshot'),

    url(r'^task/log/(?P<task_id>\w+)$', 'testing_runtime.web.tasks.log'),
    url(r'^ajax/call$', 'testing_runtime.web.api.call'),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    url(r'^user/login$', 'testing_runtime.web.user.login_page'),
    url(r'^user/logout$', 'testing_runtime.web.user.logout'),

    url(r'^github/notify$', 'testing_runtime.github.views.push_notification'),
    url(r'^github/test$', 'testing_runtime.github.views.test_notification'),

    url(r'^modules/list$', 'testing_runtime.web.modules.list_modules'),
    url(r'^modules/add$', 'testing_runtime.web.modules.add_module'),
    url(r'^modules/update/(?P<module_id>\w+)$', 'testing_runtime.web.modules.update_module'),
    url(r'^modules/remove$', 'testing_runtime.web.modules.remove_module'),
)
