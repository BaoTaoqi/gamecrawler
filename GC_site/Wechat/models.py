from django.db import models
from SteamGames.models import Depository

# Create your models here.


class WechatUser(models.Model):
    name = models.CharField(max_length=200, verbose_name='昵称')
    wechat_openid = models.CharField(max_length=200, verbose_name='openid', primary_key=True)
    password = models.CharField(max_length=200, verbose_name='密码', null=True)
    is_effective = models.BooleanField(default=True)
    c_time = models.DateTimeField()
    steam_games_subscribed = models.ManyToManyField(
        Depository,
        through='wx_SteamSubscriber',
        through_fields=('user', 'steam_game')
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '微信用户'
        verbose_name_plural = '微信用户'


class wx_SteamSubscriber(models.Model):
    user = models.ForeignKey(WechatUser, on_delete=models.CASCADE, verbose_name='订阅用户')
    steam_game = models.ForeignKey(Depository, on_delete=models.CASCADE, verbose_name='订阅游戏')
    if_notified = models.BooleanField(verbose_name='是否通知过')
