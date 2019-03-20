from . import views

from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path(
        'all',
        views.listing,
        name='categories.listing'),
    path(
        'suggested',
        views.listing_suggested,
        name='categories.listing_suggested'),
    path(
        'suggest_category',
        views.suggest_category,
        name='categories.suggest_category'),
    path(
        '<slug:slug>',
        views.all_from_category,
        name='categories.all_from_category'),
]
