from django.urls import path
from Wechat import views


urlpatterns = [
    path('', views.home),
    path('auth/', views.weixinbind),
    path('index/', views.weixinbind_callback),
]