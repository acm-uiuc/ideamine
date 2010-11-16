from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'main.views.index'),
    (r'^users/$', 'main.views.users'),
    (r'^users/(\d+)/$', 'main.views.users'),
    (r'^ideas/$', 'main.views.ideas'),
    (r'^ideas/(\d+)/$', 'main.views.ideas'),
    # Example:
    # (r'^ideamine/', include('ideamine.foo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
