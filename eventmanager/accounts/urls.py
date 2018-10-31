from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='accounts.index'),
    path('home', views.home, name='accounts.home'),
    path('signup', views.signup, name='accounts.signup'),
    path('signout', views.signout, name='accounts.signout'),
    path('login', views.login, name='accounts.login'),
]
