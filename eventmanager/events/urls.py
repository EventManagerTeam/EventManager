from . import views

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from .feeds import EventFeed
from .feeds import LatestEventFeed


urlpatterns = [
    path('export/', views.export, name='events.export'),
    path('export/csv', views.export_as_csv, name='events.export_csv'),
    path('export/json', views.export_as_json, name='events.export_json'),
    path('all/', views.index, name='events.list'),
    path('random/', views.show_random_event, name='events.show_random_event'),
    path('invites/', views.invites, name='events.invites'),
    path('tasks/', views.tasks, name='events.tasks'),
    path('create_event/', views.create_event, name='events.create_event'),
    path('my_events/', views.my_events, name='events.my_events'),
    path('hosted/', views.events_I_host, name='events.events_I_host'),
    path('list/', views.index, name='events.list'),
    path('<slug:slug>', views.show_events_by_slug, name='events.event'),
    path(
        '<slug:slug>/confirm_invite',
        views.confirm_invite,
        name='events.confirm_invite'
    ),
    path(
        '<slug:slug>/decline_invite',
        views.decline_invite,
        name='invites.decline_invite'
    ),
    path('<slug:slug>/delete', views.delete_event_by_slug, name='events.del'),
    path('<slug:slug>/board', views.event_board, name='events.board'),

    path(
        '<slug:slug>/<comment>/delete',
        views.delete_comment_by_slug,
        name='events.comment.del'
    ),

    path(
        '<slug:slug>/<comment>/edit',
        views.edit_comment_by_slug,
        name='events.comment.edit'
    ),


    path('<slug:slug>/edit', views.edit_event, name='events.edit'),
    path(
        '<slug:slug>/add_teammate',
        views.add_teammate,
        name='events.add_teammate'
    ),
    path(
        '<user>/<slug:slug>/add_teammate',
        views.event_team_add,
        name='events.event_team_add'
    ),
    path('<slug:slug>/join', views.join_event, name='events.join'),
    path('<slug:slug>/cancel_join', views.cancel_join, name='events.rm_join'),
    path(
        '<slug:slug>/settings',
        views.visibility_settings,
        name='events.settings'
    ),
    url(r'^feed/$', EventFeed(), name='event_feed'),
    url(r'^latest_feed/$', LatestEventFeed(), name='latest_event_feed'),
    path('<slug:slug>', views.show_events_by_slug, name='event'),
    path(
        'users/<slug:slug>/<event>/invite',
        views.invite,
        name='events.invite'
    ),
]
