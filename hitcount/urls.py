from __future__ import unicode_literals
from django.conf.urls import url
from hitcount.views import HitCountJSONView
app_name = 'hitcount'
urlpatterns = [url('^hit/ajax/$', HitCountJSONView.as_view(), name='hit_ajax')]
