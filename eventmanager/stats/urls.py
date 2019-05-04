from . import views

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path(
        '<slug:slug>/statistics',
        views.get_statistics,
        name='events.statistics'),
]
