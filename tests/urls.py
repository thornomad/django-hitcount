# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # for our built-in ajax post view
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
)
