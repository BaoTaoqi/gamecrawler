import re
from django.shortcuts import render
from .forms import SteamSearchForm
from SteamGames.models import Depository
from django.db.models.query import EmptyQuerySet

# Create your views here.


def index(request):
    return render(request, 'search/index.html')


def steam_search_basic(text):
    if text.isdigit():
        id_search = Depository.objects.filter(ID=int(text))
    else:
        id_search = Depository.objects.none()
    gamename_search = Depository.objects.filter(GameName__icontains=text)
    link_prepare = re.findall('https://store.steampowered.com/app/\d*/', text)
    if link_prepare == []:
        link_search = Depository.objects.none()
    else:
        link_prepare = link_prepare[0]
        link_search = Depository.objects.filter(Link=link_prepare)

    return Depository.objects.none().union(id_search, gamename_search, link_search)


def steam_search(request):
    if request.method == "POST":
        steam_search_form = SteamSearchForm(request.POST)
        if steam_search_form.is_valid():
            result = steam_search_basic(steam_search_form.cleaned_data['text'])
            return render(request, 'search/steam_search.html',
                          {'result': result, 'steam_search_form': steam_search_form})
        else:
            return render(request, 'search/steam_search.html', {'message': '你输入的数据有错误！', 'steam_search_form': steam_search_form})
    elif request.method == 'GET':
        steam_search_form = SteamSearchForm(request.GET)
        if steam_search_form.is_valid():
            result = steam_search_basic(steam_search_form.cleaned_data['text'])
            return render(request, 'search/steam_search.html',
                          {'result': result, 'steam_search_form': steam_search_form})
        else:
            return render(request, 'search/steam_search.html',
                          {'message': '你输入的数据有错误！哦没输啊，那没事了', 'steam_search_form': steam_search_form})
    else:
        steam_search_form = SteamSearchForm()
        return render(request, 'search/steam_search.html', {'message': '初始化查询', 'steam_search_form': steam_search_form})
