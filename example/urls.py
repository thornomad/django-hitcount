from django.conf.urls.defaults import patterns, include, url
from hitcount.views import update_hit_count_ajax


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.foo.urls')),

    url(r'^ajax/hit/$',
        update_hit_count_ajax,
        name='hitcount_update_ajax'), # keep this name the same

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
