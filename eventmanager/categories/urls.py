from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('all', views.listing, name='categories.listing'),
]
