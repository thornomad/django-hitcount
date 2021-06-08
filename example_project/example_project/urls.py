from django.conf.urls import include, url
from django.contrib import admin
from blog import views
admin.autodiscover()
urlpatterns = [url('^$', views.IndexView.as_view(), name='index'), url(
    '^generic-detail-view-ajax/(?P<pk>\\d+)/$', views.PostDetailJSONView.
    as_view(), name='ajax'), url('^hitcount-detail-view/(?P<pk>\\d+)/$',
    views.PostDetailView.as_view(), name='detail'), url(
    '^hitcount-detail-view-count-hit/(?P<pk>\\d+)/$', views.
    PostCountHitDetailView.as_view(), name='detail-with-count'), url(
    'hitcount/', include('hitcount.urls', namespace='hitcount'))]
try:
    urlpatterns.append(url('^admin/', include(admin.site.urls)))
except:
    urlpatterns.append(url('^admin/', admin.site.urls))
