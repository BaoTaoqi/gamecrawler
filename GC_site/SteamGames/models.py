from django.db import models
import hashlib


# Create your models here.

class Depository(models.Model):
    ID = models.IntegerField(verbose_name='游戏ID')
    Link = models.CharField(max_length=100, verbose_name='游戏链接')
    GameName = models.CharField(max_length=200, verbose_name='游戏名称', primary_key=True)
    BundleBaseDiscount = models.CharField(max_length=20, verbose_name='基本折扣力度')
    DiscountPct = models.CharField(max_length=20, verbose_name='现有折扣力度')
    OriginalPrice = models.CharField(max_length=20, verbose_name='原价')
    FinalPrice = models.CharField(max_length=20, verbose_name='现价')
    LowestPrice = models.CharField(max_length=20, verbose_name='史低')
    LastPrice = models.CharField(max_length=20, verbose_name='上次价格')
    IfHandle = models.BooleanField(verbose_name='是否处理')

    def __str__(self):
        return self.GameName


class ErrorCheck(models.Model):
    ID = models.IntegerField(verbose_name='游戏ID')
    Link = models.CharField(max_length=100, verbose_name='游戏链接')
    GameName = models.CharField(max_length=200, verbose_name='游戏名称', primary_key=True)
    BundleBaseDiscount = models.CharField(max_length=20, verbose_name='基本折扣力度')
    DiscountPct = models.CharField(max_length=20, verbose_name='现有折扣力度')
    OriginalPrice = models.CharField(max_length=20, verbose_name='原价')
    FinalPrice = models.CharField(max_length=20, verbose_name='现价')
    LowestPrice = models.CharField(max_length=20, verbose_name='史低')
    LastPrice = models.CharField(max_length=20, verbose_name='上次价格')
    IfHandle = models.BooleanField(verbose_name='是否处理')

    def __str__(self):
        return self.GameName
