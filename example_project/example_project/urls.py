from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from blog import views
from hitcount.views import update_hit_count_ajax


urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^(?P<post_id>\d+)/$', views.detail, name='detail'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^ajax/hit/$', # you can change this url if you would like
        update_hit_count_ajax,
        name='hitcount_update_ajax'), # keep this name the same

)
