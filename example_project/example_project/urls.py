from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from blog import views
from hitcount.views import update_hit_count_ajax


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name="index"),
    url(r'^(?P<post_id>\d+)/$', views.detail, name='detail'),

    # for our built-in ajax post view
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

)
