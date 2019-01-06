from . import views

from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('all', views.listing, name='categories.listing'),
    path('<slug:slug>', views.all_from_category,
         name='categories.all_from_category'),
]
