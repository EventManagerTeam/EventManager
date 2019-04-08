from . import views

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path(
        'events/export/',
        views.export,
        name='exporting/export'),
    path(
        'events/export/csv',
        views.export_as_csv,
        name='exporting/export_csv'),
    path(
        'events/export/json',
        views.export_as_json,
        name='exporting/export_json'),
]
