from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('all/', views.index, name='events.list'),
    path('list/', views.index, name='events.list'),
    path('<slug:slug>', views.show_events_by_slug, name='article'),
]
