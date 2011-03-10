from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import list_detail, create_update
from django.conf import settings
from main.models import Idea, User
from main.forms import *

admin.autodiscover()

users = { 'queryset' : User.objects.all() }
ideas = { 'queryset' : Idea.objects.all() }

urlpatterns = patterns('',
    (r'^$', 'main.views.index'),

    (r'^tags/suggest', 'main.views.tag_suggest', {}, 'tag_suggest'),

    (r'^users/(?P<object_id>\d+)/update', 'main.views.user_update', {}, 'user_update'),
    (r'^users/(?P<object_id>\d+)', 'main.views.user_detail', users, 'user_detail'),
    (r'^users/self', 'main.views.redirect_to_user', {}, 'user_detail_self'),
    (r'^users/create', 'main.views.user_create', {}, 'user_create'),
    (r'^users', list_detail.object_list, users, 'user_list'),

    (r'^ideas/(?P<object_id>\d+)/members', 'main.views.members'),
    (r'^ideas/(?P<object_id>\d+)/join', 'main.views.idea_join', {}, 'user_join_idea'),
    (r'^ideas/(?P<object_id>\d+)/leave', 'main.views.idea_leave', {}, 'user_leave_idea'),
    (r'^ideas/(?P<object_id>\d+)/update', 'main.views.idea_update', {}, 'idea_update'),
    (r'^ideas/(?P<object_id>\d+)/confirm/(?P<member_id>\d+)', 'main.views.confirm_member', {}, 'idea_confirm_member'),
    (r'^ideas/(?P<object_id>\d+)', 'main.views.idea_detail', {}, 'idea_detail'),
    (r'^ideas/create', 'main.views.idea_create', {}, 'idea_create'),
    (r'^ideas', list_detail.object_list, ideas, 'idea_list'),

    (r'^comments', include('django.contrib.comments.urls')),

    (r'^login', 'django.contrib.auth.views.login', {}, 'login'),
    (r'^logout', 'django.contrib.auth.views.logout',
     { 'next_page' : '/'}, 'logout'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)', 'django.views.static.serve',
            { 'document_root' : settings.STATIC_ROOT }),
    )
