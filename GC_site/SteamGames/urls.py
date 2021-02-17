from django.urls import path
from . import views

app_name = 'SteamGames'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:game_id>/', views.id_detail, name='id_detail'),
    path('<int:game_id>/<str:game_name>/', views.game_detail, name='game_detail'),
    path('<int:game_id>/<str:game_name>/subscribe/', views.subscribe, name='subscribe'),
    path('<int:game_id>/<str:game_name>/unsubscribe/', views.unsubscribe, name='unsubscribe'),
]
