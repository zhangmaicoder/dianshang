from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    age = models.IntegerField(default=18, verbose_name='用户年龄')
    gender = models.CharField(max_length=10, default='男', verbose_name='用户性别')
    nickname = models.CharField(max_length=10, verbose_name='用户昵称')
    phone = models.CharField(max_length=50, default="123456", verbose_name='电话号码')
    headers = models.ImageField(upload_to='static/images/headers/', default='static/images/headers/default.jpg', verbose_name='用户头像', )
    # 一对一外键
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users_userinfo'
        verbose_name_plural = "用户"


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    recv_name = models.CharField(max_length=100, verbose_name="收货人")
    recv_tel = models.CharField(max_length=20, verbose_name="收货电话")
    province = models.CharField(max_length=100, verbose_name="收货人省份")
    city = models.CharField(max_length=100, verbose_name="收货城市")
    area = models.CharField(max_length=255, verbose_name="收货人县区")
    street = models.CharField(max_length=255, verbose_name="收货人街道")
    status = models.BooleanField(default=False, verbose_name="是否是默认地址")
    desc = models.CharField(max_length=255, verbose_name="详细地址")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="地址所属用户")

    class Meta:
        db_table = 'users_address'
        verbose_name_plural = "用户地址"

