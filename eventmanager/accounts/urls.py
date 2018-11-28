from . import views
from django.conf.urls import url
from django.urls import path


urlpatterns = [
    path('', views.index, name='accounts.index'),
    path('home', views.home, name='accounts.home'),
    path('signup', views.signup, name='accounts.signup'),
    path('signout', views.signout, name='accounts.signout'),
    path('login', views.login, name='accounts.login'),
    path('account', views.account_details, name='accounts.account'),
    path(
        'edit_account',
        views.edit_account_details,
        name='accounts.edit_account_details'
    ),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(
        r'^account_details/$',
        views.show_account_details,
        name='accounts.details'
    ),

    url(r'^change_email/$', views.change_email, name='change_email'),
    path('users', views.list_users, name='accounts.list_users'),
    path(
        'users/<slug:slug>',
        views.gеt_user_by_slug,
        name='accounts.list_users'
    ),
    path('users/<slug:slug>/friend', views.friend, name='accounts.add_friend'),
    path(
        'users/<slug:slug>/unfriend',
        views.unfriend,
        name='accounts.unfriend'
    ),
    path('friends', views.my_friends, name='events.my_friends'),

    path('friends/find', views.search_users, name='events.search_users'),

]
