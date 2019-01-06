from . import views

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path(
        'events/<slug:slug>/task/<task>/delete/',
        views.delete_task,
        name='tasks.delete_task'),
    path(
        'events/<slug:slug>/task/<task>/edit',
        views.edit_task,
        name='tasks.edit_task'),
]
