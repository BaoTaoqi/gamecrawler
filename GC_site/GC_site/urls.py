"""GC_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('MP_verify_zyyETcTfFeD3eONC.txt', TemplateView.as_view(template_name='MP_verify_zyyETcTfFeD3eONC.txt', content_type='text/plain')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon/favicon.ico')),
    path('GC_controller/', admin.site.urls),
    path('', include('GameCrawler.urls')),
    path('search/', include('search.urls')),
    path('captcha', include('captcha.urls')),
    path('polls/', include('polls.urls')),
    path('wechat/', include('Wechat.urls')),
    path('steamgames/', include('SteamGames.urls')),
]
