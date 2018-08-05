from django.db import models
from users.models import UserModel


class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    isDelete = models.IntegerField(default=1)
    class_type = models.CharField(max_length=50)
    type_pic =models.CharField(max_length=200)

    class Meta:
        db_table = 'goods_type'


# 商品模型
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.CharField(max_length=200)
    gprice = models.FloatField(default=0)
    isDelete = models.IntegerField(default=1)
    danwei = models.CharField(max_length=20, default='500g')
    zhuangtai = models.IntegerField()
    jieshao = models.CharField(max_length=200)
    kucun = models.IntegerField(default=0)
    guanjianzi = models.CharField(max_length=200)
    gtype = models.ForeignKey(TypeInfo)

    class Meta:
        db_table= 'goods'


class CartInfo(models.Model):
    user = models.ForeignKey(UserModel)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()

    class Meta:
        db_table = 'cart'