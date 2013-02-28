from django.conf.urls import patterns, url, include
import settings

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),

    url( r'', include("testing_runtime.urls") ),

    (r'^i18n/', include('django.conf.urls.i18n')),

)
