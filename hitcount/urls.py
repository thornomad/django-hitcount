# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from hitcount.views import update_hit_count_ajax

urlpatterns = [
    url(r'^hit/ajax/$', update_hit_count_ajax, name='hit_ajax'),
]
