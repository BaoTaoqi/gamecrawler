from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from Wechat.models import WechatUser, wx_SteamSubscriber
from .forms import UserForm, RegisterForm
from django.conf import settings
from django.utils import timezone
import hashlib
import datetime
import uuid


# Create your views here.


def index(request):
    pass
    return render(request, 'GameCrawler/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect("/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:
                    message = "该用户还未通过邮件确认！"
                    return render(request, 'GameCrawler/login/login.html', locals())
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['wx_is_login'] = False
                    request.session['user_openid'] = user.web_openid
                    request.session['user_name'] = user.name
                    return redirect('/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'GameCrawler/login/login.html', locals())

    login_form = UserForm()
    return render(request, 'GameCrawler/login/login.html', locals())


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


def register(request):
    if request.session.get('is_login', None):
        return redirect("/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            password_ensure = register_form.cleaned_data['password_ensure']
            email = register_form.cleaned_data['email']
            if password != password_ensure:
                message = "两次输入密码不同！"
                return render(request, 'GameCrawler/login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'GameCrawler/login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'GameCrawler/login/register.html', locals())

                new_user = models.User.objects.create(
                    web_openid=uuid.uuid3(uuid.NAMESPACE_URL, username),
                    name=username,
                    password=hash_code(password),
                    email=email,
                    c_time=datetime.datetime.now()
                )

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往注册邮箱，进行邮件确认！'
                return render(request, 'GameCrawler/login/confirm.html', locals())
    register_form = RegisterForm()
    return render(request, 'GameCrawler/login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/')
    request.session.flush()
    return redirect('/')


def hash_code(password, salt='GC_site'):
    password_hashed = hashlib.sha256()
    password += salt
    password_hashed.update(password.encode())
    return password_hashed.hexdigest()


def send_email(mail_to, code):
    from django.core.mail import EmailMultiAlternatives

    from_mail = 'account-register@mail.gamecrawler.top'
    subject = 'GameCrawler账户验证'
    text_content = ''
    html_content = '<p>你的GameCrawler账户注册成功！请点击<a href="http://www.gamecrawler.top/confirm/?code={}" target=blank>此处</a>验证你的账户，有效期为{}天。如果你没有注册，请忽略这条消息。</p>'.format(code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, from_mail, [mail_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'GameCrawler/login/confirm.html', locals())

    c_time = confirm.c_time
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'GameCrawler/login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'GameCrawler/login/confirm.html', locals())


def user_management(request, user_openid):
    return render(request, 'GameCrawler/user/user_management.html')


def subscribe_management(request, user_openid):
    return render(request, 'GameCrawler/user/subscribe_management.html')


def steam_subscribe_list(request, user_openid):
    if request.session['is_login']:
        user = models.User.objects.get(web_openid=user_openid)
        notified_subscribed_steam_games = user.steam_games_subscribed.filter(steamsubscriber__if_notified=1)
        not_notified_subscribed_steam_games = user.steam_games_subscribed.filter(steamsubscriber__if_notified=0)
    if request.session['wx_is_login']:
        user = WechatUser.objects.get(wechat_openid=user_openid)
        notified_subscribed_steam_games = user.steam_games_subscribed.filter(wx_steamsubscriber__if_notified=1)
        not_notified_subscribed_steam_games = user.steam_games_subscribed.filter(wx_steamsubscriber__if_notified=0)
    notified_hashed_names = user.steam_games_subscribed.filter(steamsubscriber__if_notified=1)
    for name in notified_hashed_names:
        name.GameName = hash_code(name.GameName, salt='SteamGames')
    not_notified_hashed_names = user.steam_games_subscribed.filter(steamsubscriber__if_notified=0)
    for name in not_notified_hashed_names:
        name.GameName = hash_code(name.GameName, salt='SteamGames')
    return render(request, 'GameCrawler/user/steam_subscribe_list.html',
                  {
                      'notified_subscribed_steam_games': notified_subscribed_steam_games,
                      'not_notified_subscribed_steam_games': not_notified_subscribed_steam_games,
                      'notified_hashed_names': notified_hashed_names,
                      'not_notified_hashed_names': not_notified_hashed_names,
                  })
