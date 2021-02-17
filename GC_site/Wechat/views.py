import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import WechatUser
import urllib.parse
import datetime
import json

APPID = ''
APPSECRET = ''
REDIRECT_URI = urllib.parse.quote('', safe='')


def home(request):
    pass
    return render(request, 'GameCrawler/index.html')


def weixinbind(request):
    return HttpResponseRedirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_userinfo#wechat_redirect'.format(APPID, REDIRECT_URI))


def weixinbind_callback(request):
    code = request.GET.get('code')
    requests_get = requests.get(
        'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(APPID, APPSECRET, code)
    )
    json_loads = json.loads(requests_get.text)
    requests_get = requests.get(
        'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (json_loads['access_token'], json_loads['openid'])
    )
    user_data = json.loads(requests_get.content.decode('utf8'))
    user = WechatUser.objects.filter(is_effective=True).filter(wechat_openid=user_data['openid'])
    if user.count() == 0:
        user = WechatUser.objects.create(name=user_data['nickname'],
                                         wechat_openid=user_data['openid'],
                                         password='',
                                         c_time=datetime.datetime.now()
                                         )
        request.session['wx_is_login'] = True
        request.session['is_login'] = False
        request.session['wx_user_openid'] = user.wechat_openid
        request.session['wx_user_name'] = user.name
    else:
        request.session['wx_is_login'] = True
        request.session['is_login'] = False
        request.session['wx_user_id'] = user.first().wechat_openid
        request.session['wx_user_name'] = user.first().name
    return home(request)
