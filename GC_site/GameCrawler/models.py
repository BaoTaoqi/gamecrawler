from django.db import models
from SteamGames.models import Depository


# Create your models here.


class User(models.Model):
    web_openid = models.CharField(max_length=200, verbose_name='openid', primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField()
    has_confirmed = models.BooleanField(default=False)
    steam_games_subscribed = models.ManyToManyField(
        Depository,
        through='SteamSubscriber',
        through_fields=('user', 'steam_game')
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class SteamSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='订阅用户')
    steam_game = models.ForeignKey(Depository, on_delete=models.CASCADE, verbose_name='订阅游戏')
    if_notified = models.BooleanField(verbose_name='是否通知过')


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
