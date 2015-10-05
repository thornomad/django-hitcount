# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

from blog import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # for our built-in ajax post view
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),

    # for our selenium tests
    url(r'^$', views.index, name="index"),
    url(r'^(?P<post_id>\d+)/$', views.detail, name='detail'),
]
