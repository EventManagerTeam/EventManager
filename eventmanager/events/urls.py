from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url

from .feeds import EventFeed
from .feeds import LatestEventFeed


urlpatterns = [
    path('all/', views.index, name='events.list'),
    path('invites/', views.invites, name='events.invites'),
    path('create_event/', views.create_event, name='events.create_event'),
    path('list/', views.index, name='events.list'),
    path('<slug:slug>', views.show_events_by_slug, name='events.event'),
    path(
        '<slug:slug>/confirm_invite',
        views.confirm_invite,
        name='events.confirm_invite'
    ),
    path('<slug:slug>/delete', views.delete_event_by_slug, name='events.del'),
    path('<slug:slug>/edit', views.edit_event, name='events.edit'),
    path('<slug:slug>/add_teammate', views.add_teammate, name='events.add_teammate'),
    path('<user>/<slug:slug>/add_teammate', views.event_team_add, name='events.event_team_add'),
    path('<slug:slug>/join', views.join_event, name='events.join'),
    path('<slug:slug>/cancel_join', views.cancel_join, name='events.rm_join'),
    url(r'^feed/$', EventFeed(), name='event_feed'),
    url(r'^latest_feed/$', LatestEventFeed(), name='latest_event_feed'),
    path('<slug:slug>', views.show_events_by_slug, name='event'),
    path(
        'users/<slug:slug>/<event>/invite',
        views.invite,
        name='events.invite'
    ),
]
