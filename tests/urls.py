# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # for our built-in ajax post view
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
]
