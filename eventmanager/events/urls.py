from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('all/', views.index, name='events.list'),
    path('create_event/', views.create_event, name='events.create_event'),
    path('list/', views.index, name='events.list'),
    path('<slug:slug>', views.show_events_by_slug, name='events.event'),
    path('<slug:slug>/delete', views.delete_event_by_slug, name='events.del'),
    path('<slug:slug>/edit', views.edit_event, name='events.edit'),
]
