from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import patterns, include, url
from nowcharleyworks import views
urlpatterns = patterns(
    '',
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True,
    }),
)

urlpatterns += patterns(
    'nowcharleyworks.views',
    url(
        r'^$',
        'index',
        name='index'
    ),
    url(
        r'^thing/save/$',
        'save',
        name='save'
    ),
    url(
        r'^thing/delete/$',
        'delete',
        name='delete'
    ),
    url(
        r'^thing/archive/$',
        'archive',
        name='archive'
    ),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns(
    'rockbot.views',
    url(
        r'^rockbot/$',
        'rockbot',
        name='rockbot'
    ),
)
