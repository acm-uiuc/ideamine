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

    (r'^users/(?P<object_id>\d+)', list_detail.object_detail, users, 'user_detail'),
    (r'^users', list_detail.object_list, users, 'user_list'),

    (r'^ideas/(?P<object_id>\d+)/members', 'main.views.members'),
    (r'^ideas/(?P<object_id>\d+)/join', 'main.views.idea_join', {}, 'user_join_idea'),
    (r'^ideas/(?P<object_id>\d+)', list_detail.object_detail, ideas, 'idea_detail'),
    (r'^ideas/create', 'main.views.idea_create', {}, 'idea_create'),
    (r'^ideas', list_detail.object_list, ideas, 'idea_list'),

    (r'^comments', include('django.contrib.comments.urls')),

    (r'^login', 'django.contrib.auth.views.login', {}, 'login'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)', 'django.views.static.serve',
            { 'document_root' : settings.STATIC_ROOT }),
    )
