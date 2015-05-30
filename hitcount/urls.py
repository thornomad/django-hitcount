# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from hitcount.views import update_hit_count_ajax

urlpatterns = patterns('',
    url(r'^hit/ajax/$', update_hit_count_ajax, name='hit_ajax'),
)
