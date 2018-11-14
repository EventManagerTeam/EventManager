from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('all', views.listing, name='categories.listing'),
    path('<slug:slug>', views.all_from_category,
         name='categories.all_from_category'),
]
