from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^$', 'ganymede.views.home'),
    url(r'^ajax/test$', 'ganymede.views.test'),
    url(r'^.*\.png', 'ganymede.views.screenshot'),
)
