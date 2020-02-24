from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    # 用户登录
    url(r"^login/$", views.user_login, name="user_login"),
    # 主页
    url(r"^index/$", views.index, name="index"),
    # 用户注册
    url(r"^register/$", views.register, name="register"),
    # # 用户退出
    url(r"^logout/$", views.logout, name="logout"),
    # 产生验证码
    url(r"^createCode/$", views.createCode, name="createCode"),
    # 用户中心-信息页
    url(r'^user_center_info/$', views.user_center_info, name='user_center_info'),
    url(r'^user_alter_info/$', views.user_alter_info, name='user_alter_info'),
    url(r'^watch/$', views.watch, name='watch'),

    # 用户中心-密码修改页
    url(r'^set_password/$', views.set_password, name='set_password'),

    url(r'^add_address/$', views.add_address, name='add_address'),
    url(r'^address_list/$', views.address_list, name='address_list'),

]
