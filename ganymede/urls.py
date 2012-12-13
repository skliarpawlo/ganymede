from django.conf.urls import patterns, url, include
import settings

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
        }),
    url(r'^$', 'ganymede.views.home'),
    url(r'^ajax/test$', 'ganymede.views.test'),
    url(r'^.*\.png', 'ganymede.views.screenshot'),
)
