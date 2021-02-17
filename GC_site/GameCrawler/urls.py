from django.urls import path, re_path
from . import views

app_name = 'GameCrawler'
urlpatterns = [
    path('', views.index),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    re_path(r'^confirm/$', views.user_confirm),
    path('user_management/<str:user_openid>/', views.user_management, name='user_management'),
    path('user_management/<str:user_openid>/subscribe_management', views.subscribe_management, name='subscribe_management'),
    path('user_management/<str:user_openid>/steam_subscribe_list', views.steam_subscribe_list, name='steam_subscribe_list'),
]
