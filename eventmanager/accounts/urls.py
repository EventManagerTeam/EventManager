from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='accounts.index'),
    path('signup', views.signup, name='accounts.signup'),
]
