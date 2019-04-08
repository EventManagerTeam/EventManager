from . import views

from django.conf.urls import url
from django.urls import path


urlpatterns = [
    path('home', views.home, name='accounts.home'),
    path('', views.index, name='accounts.index'),
]
