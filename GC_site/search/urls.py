from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('steam_search/', views.steam_search, name='steam_search'),
]
