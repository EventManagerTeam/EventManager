from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='accounts.index'),
    path('home', views.home, name='accounts.home'),
    path('signup', views.signup, name='accounts.signup'),
    path('signout', views.signout, name='accounts.signout'),
    path('login', views.login, name='accounts.login'),
    url(r'^change_password/$', views.change_password, name='change_password'),
]
