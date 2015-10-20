# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from hitcount.views import HitCountJSONView

urlpatterns = [
    url(r'^hit/ajax/$', HitCountJSONView.as_view(), name='hit_ajax'),
]
