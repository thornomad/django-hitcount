# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

from blog import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name="index"),
    url(r'^(?P<post_id>\d+)/$', views.detail, name='detail'),

    # for our built-in ajax post view
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
]
