from django.db import models
import goods
from django.contrib.auth.models import  User


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    goods = models.ForeignKey(goods.models.Goods, verbose_name="购物车商品")
    count = models.IntegerField(verbose_name="商品数量")
    addTime = models.DateTimeField(auto_now_add=True, verbose_name="商品添加时间")
    allTotal = models.FloatField()
    user = models.ForeignKey(User)

