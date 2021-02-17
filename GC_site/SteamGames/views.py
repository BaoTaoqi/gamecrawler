from django.shortcuts import render
from django.views import generic
from .models import Depository
from GameCrawler.models import User, SteamSubscriber
from Wechat.models import WechatUser, wx_SteamSubscriber
from .forms import SubscribeForm
import hashlib


class IndexView(generic.ListView):
    template_name = 'SteamGames/index.html'
    context_object_name = 'random_games_list'

    def get_queryset(self):
        return Depository.objects.order_by('?')[:20]


def hash_code(game_name, salt='SteamGames'):
    game_name_hashed = hashlib.sha256()
    game_name += salt
    game_name_hashed.update(game_name.encode())
    return game_name_hashed.hexdigest()


def id_detail(request, game_id):
    games = Depository.objects.filter(ID=game_id)
    new_games = Depository.objects.filter(ID=game_id)
    for game in new_games:
        game.GameName = hash_code(game.GameName)
    return render(request, 'SteamGames/id_detail.html', {'games': games, 'new_games': new_games})


def game_detail(request, game_id, game_name, message=None):
    subscribe_form = SubscribeForm()
    games = Depository.objects.filter(ID=game_id)
    for game in games:
        if hash_code(game.GameName) == game_name:
            new_games = Depository.objects.filter(GameName=game.GameName)
            for new_game in new_games:
                new_game.GameName = hash_code(new_game.GameName)
                return render(request, 'SteamGames/game_detail.html', {'message': message, 'game': game, 'new_game': new_game, 'subscribe_form': subscribe_form})


def subscribe(request, game_id, game_name):
    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            steam_games = Depository.objects.filter(ID=game_id)
            for steam_game in steam_games:
                if hash_code(steam_game.GameName) == game_name:
                    game = Depository.objects.get(GameName=steam_game.GameName)
                    if request.session['is_login']:
                        user = User.objects.get(web_openid=request.session['user_openid'], name=request.session['user_name'])
                        re_notify = SteamSubscriber.objects.filter(steam_game=game, user=user, if_notified=1)
                        if list(re_notify) != []:
                            re_notify[0].if_notified = 0
                            re_notify[0].save()
                            return game_detail(request, game_id, game_name, message='游戏续订成功！')
                        if list(SteamSubscriber.objects.filter(steam_game=game, user=user)) == []:
                            SteamSubscriber.objects.create(if_notified=False, steam_game=game, user=user)
                            return game_detail(request, game_id, game_name, message='游戏订阅成功！')
                        else:
                            return game_detail(request, game_id, game_name, message='你已订阅该游戏！')
                    if request.session['wx_is_login']:
                        user = WechatUser.objects.get(wechat_openid=request.session['wx_user_openid'], name=request.session['wx_user_name'])
                        re_notify = wx_SteamSubscriber.objects.filter(steam_game=game, user=user, if_notified=1)
                        if list(re_notify) != []:
                            re_notify[0].if_notified = 0
                            re_notify[0].save()
                        if list(wx_SteamSubscriber.objects.filter(steam_game=game, user=user)) == []:
                            wx_SteamSubscriber.objects.create(if_notified=False, steam_game=game, user=user)
                            return game_detail(request, game_id, game_name, message='游戏订阅成功！')
                        else:
                            return game_detail(request, game_id, game_name, message='你已订阅该游戏！')

                # else:
                    # return game_detail(request, game_id, game_name, message='游戏检索错误！')
        else:
            return game_detail(request, game_id, game_name, message='确认码错误！')


def unsubscribe(request, game_id, game_name):
    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            steam_games = Depository.objects.filter(ID=game_id)
            for steam_game in steam_games:
                if hash_code(steam_game.GameName) == game_name:
                    game = Depository.objects.get(GameName=steam_game.GameName)
                    if request.session['is_login']:
                        user = User.objects.get(web_openid=request.session['user_openid'],
                                                name=request.session['user_name'])
                        if list(SteamSubscriber.objects.filter(steam_game=game, user=user)) == []:
                            return game_detail(request, game_id, game_name, message='你未订阅该游戏！')
                        else:
                            user.steam_games_subscribed.remove(game)
                            return game_detail(request, game_id, game_name, message='游戏退订成功！')
                    if request.session['wx_is_login']:
                        user = WechatUser.objects.get(wechat_openid=request.session['wx_user_openid'],
                                                      name=request.session['wx_user_name'])
                        if list(wx_SteamSubscriber.objects.filter(steam_game=game, user=user)) == []:
                            return game_detail(request, game_id, game_name, message='你未订阅该游戏！')
                        else:
                            user.steam_games_subscribed.remove(game)
                            return game_detail(request, game_id, game_name, message='游戏退订成功！')
                # else:
                    # return game_detail(request, game_id, game_name, message='游戏检索错误！')
        else:
            return game_detail(request, game_id, game_name, message='确认码错误！')
