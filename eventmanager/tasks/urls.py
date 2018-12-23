from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url


urlpatterns = [
    path(
        'events/<slug:slug>/task/<task>/delete',
        views.delete_task,
        name='tasks.delete_task'),
]
