from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()
from birding_ear import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'birding_ear.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'birding_ear.views.index'),
    url(r'^bird_detail/(?P<bird_name_slug>[\w\-]+)/$', 'birding_ear.views.bird_detail'),
    url(r'^mix_detail/(?P<mix_nickname_slug>[\w\-]+)/$', 'birding_ear.views.mix_detail'),
    url(r'^mix_settings/(?P<mix_nickname_slug>[\w\-]+)/$', 'birding_ear.views.mix_settings'),
    url(r'^ajax/', views.ajax, name="ajax"),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^dom$', views.dom, name="dom"),
)
