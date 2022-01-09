from django.urls import path

from hitcount.views import HitCountJSONView

app_name = 'hitcount'

urlpatterns = [
    path('hit/ajax/', HitCountJSONView.as_view(), name='hit_ajax'),
]
