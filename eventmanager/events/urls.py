from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('all/', views.index, name='events.list'),
]
