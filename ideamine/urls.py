from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import list_detail
from django.conf import settings
from main.models import Idea, User

admin.autodiscover()

users = { 'queryset' : User.objects.all() }
ideas = { 'queryset' : Idea.objects.all() }

urlpatterns = patterns('',
    (r'^$', 'main.views.index'),

    (r'^users/$', list_detail.object_list,
     dict(users, template_name='users.html')),
    (r'^users/(?P<object_id>\d+)/$', list_detail.object_detail,
     dict(users, template_name='user.html')),

    (r'^ideas/$', list_detail.object_list,
     dict(ideas, template_name="ideas.html")),
    (r'^ideas/(?P<object_id>\d+)/$', list_detail.object_detail,
     dict(ideas, template_name='idea.html', template_object_name='idea')),
    (r'^ideas/(?P<object_id>\d+)/members/$', 'main.views.members'),

    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)', 'django.views.static.serve',
            { 'document_root' : settings.STATIC_ROOT }),
    )
