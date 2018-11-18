from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url

from .feeds import EventFeed
from .feeds import LatestEventFeed


urlpatterns = [
    path('all/', views.index, name='events.list'),
    path('create_event/', views.create_event, name='events.create_event'),
    path('list/', views.index, name='events.list'),
    path('<slug:slug>', views.show_events_by_slug, name='events.event'),
    path('<slug:slug>/delete', views.delete_event_by_slug, name='events.del'),
    url(r'^feed/$', EventFeed(), name='event_feed'),
    url(r'^latest_feed/$', LatestEventFeed(), name='latest_event_feed'),

]
