from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import list_detail
from main.models import Idea, User

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'main.views.index'),
    (r'^users/$', list_detail.object_list, {"queryset" : User.objects.all(), "template_name" : "users.html"}),
    (r'^users/(\d+)/$', 'main.views.user'),
    (r'^ideas/$', list_detail.object_list, {"queryset" : Idea.objects.all(), "template_name" : "ideas.html"}),
    (r'^ideas/(\d+)/$', 'main.views.idea'),
    # Example:
    # (r'^ideamine/', include('ideamine.foo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
