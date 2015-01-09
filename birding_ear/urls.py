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
    url(r'^$', 'birding_ear.views.index', name="index"),
    url(r'^bird_detail/(?P<bird_name_slug>[\w\-]+)/$', 'birding_ear.views.bird_detail'),
    url(r'^mix_detail/(?P<mix_id_slug>[\w\-]+)/$', 'birding_ear.views.mix_detail'),
    url(r'^mix_settings_edit/(?P<mix_id_slug>[\w\-]+)/$', 'birding_ear.views.mix_settings_edit'),
    url(r'^mix_settings_new?$', 'birding_ear.views.mix_settings_new'),
    url(r'^register?$', 'birding_ear.views.register', name="register"),
    url(r'^login?$', 'birding_ear.views.login', name="login"),
    url(r'^logout?$', 'birding_ear.views.logout_view', name="logout"),
    url(r'^favorites?$', 'birding_ear.views.favorites', name="favorites"),
    url(r'^settings?$', 'birding_ear.views.settings', name="settings"),
    url(r'^drill/(?P<mix_id_slug>[\w\-]+)/$', 'birding_ear.views.drill'),
    url(r'^mix_drill_birds/(?P<mix_id_slug>[\w\-]+)/$', views.mix_drill_birds, name="mix_drill_birds"),
    url(r'^ajax/', views.ajax, name="ajax"),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^dom$', views.dom, name="dom"),


)
