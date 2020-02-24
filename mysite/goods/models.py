from django.db import models
import store


class GoodsType(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='商品类型id')
    name = models.CharField(max_length=255,unique=True, verbose_name='商品类型名称')
    cover = models.ImageField(upload_to='static/images/goods', default='static/images/goods/14.jpg', verbose_name="商品图片")
    intro = models.TextField(verbose_name="商品类别描述")
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="父级类型", on_delete=models.CASCADE)


class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,verbose_name="商品名称")
    # price = models.DecimalField()
    price = models.FloatField(verbose_name="商品单价")
    stock = models.IntegerField()
    count = models.IntegerField(default=0)
    createTime = models.DateTimeField(auto_now_add=True)
    intro = models.TextField()
    stores = models.ForeignKey(store.models.Store, on_delete=models.CASCADE, verbose_name="商品所属")
    goodsType = models.ForeignKey(GoodsType,on_delete=models.CASCADE, verbose_name="商品类型")


class GoodsImage(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.ImageField(upload_to='static/images/goods', default='static/images/goods/14.jpg', verbose_name="商品图片")
    status = models.BooleanField(default=False,verbose_name="是否显示默认图片")
    intro = models.TextField(verbose_name="商品图片描述")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="所属商品")
