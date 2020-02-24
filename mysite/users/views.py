from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET,require_POST
from .models import UserInfo
from django.contrib.auth import hashers
# 分页
from django.core.paginator import Paginator
# 验证码
from . import models
from . import utils
from io import BytesIO
import re
from goods.models import GoodsType, Goods


# 验证码
def createCode(req):
    # 在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = utils.create_code()
    req.session['code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


@login_required
def index(request):
    # 第一个一级类型数据
    good_type1 = GoodsType.objects.filter(pk=10001)
    good_type1_2 = GoodsType.objects.filter(parent=good_type1)
    goods1_list = Goods.objects.filter(goodsType__in=good_type1_2)


    # 第二个一级类型数据
    good_type2 = GoodsType.objects.filter(pk=10002)
    good_type2_2 = GoodsType.objects.filter(parent=good_type2)
    goods2_list = Goods.objects.filter(goodsType__in=good_type2_2)

    # 第三个一级类型数据
    good_type3 = GoodsType.objects.filter(pk=10003)
    good_type3_2 = GoodsType.objects.filter(parent=good_type3)
    goods3_list = Goods.objects.filter(goodsType__in=good_type3_2)

    # 第四个一级类型数据
    good_type4 = GoodsType.objects.filter(pk=10004)
    good_type4_2 = GoodsType.objects.filter(parent=good_type4)
    goods4_list = Goods.objects.filter(goodsType__in=good_type4_2)

    # 第五个一级类型数据
    good_type5 = GoodsType.objects.filter(pk=10005)
    good_type5_2 = GoodsType.objects.filter(parent=good_type5)
    goods5_list = Goods.objects.filter(goodsType__in=good_type5_2)

    # 第六个一级类型数据
    good_type6 = GoodsType.objects.filter(pk=10006)
    good_type6_2 = GoodsType.objects.filter(parent=good_type6)
    goods6_list = Goods.objects.filter(goodsType__in=good_type6_2)

    allGoodsType = GoodsType.objects.filter(parent__isnull=True)
    return render(request, "users/index.html", {"allGoodsType": allGoodsType,\
                                                "goods1_list": goods1_list,\
                                                "goods2_list": goods2_list,\
                                                "goods3_list": goods3_list,\
                                                "goods4_list": goods4_list,\
                                                "goods5_list": goods5_list,\
                                                "goods6_list": goods6_list})


# 用户注册
def register(request):
    if request.method == "GET":
        return render(request, 'users/register.html')
    elif request.method == "POST":
        username = request.POST['user_name'].strip()
        password = request.POST['pwd'].strip()
        confirm = request.POST['cpwd'].strip()
        email = request.POST.get("email")
        code = request.POST['code'].strip()
        if code != request.session['code']:
            return render(request, "users/register.html", {"error": "验证码错误，请重新输入"})
        if username == '':
            return render(request, 'users/register.html', {'error': '用户名不能为空！'})
        if len(password) < 6:
            return render(request, 'users/register.html', {'error': '密码小于6位'})
        if password != confirm:
            return render(request, 'users/register.html', {'error': '两次密码不一致！'})
        try:
            # 判断用户名是否已注册 get 查找到0或多条都会报错
            User.objects.get(username=username)
            return render(request, 'users/register.html', {'error': '用户名已存在'})
        except:
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                userinfo = models.UserInfo(user=user, )
                userinfo.save()
                # 跳转到登录页面
                # return redirect('user:user_login')
                return render(request, "users/login.html", {"error": "注册成功,请登录!"})
            except Exception as e:
                return render(request, "users/register.html", {"error": "注册失败!"})


# 用户登录
def user_login(request):
    if request.method == "GET":
        # 判断是否记住用户名
        if "username" in request.COOKIES:
            username = request.COOKIES.get("username")
            checked = "checked"
        else:
            username = ""
            checked = ""
        context = {
            "username": username,
            "checked": checked
        }
        return render(request, 'users/login.html', context)
    elif request.method == "POST":
        username = request.POST.get("username")
        # username = str(username).encode('utf-8')

        password = request.POST.get("pwd")
        if not all([username, password]):
            return render(request, "users/login.html", {"error": "数据不完整"})
        user = authenticate(username=username, password=password)

        if user is not None:

            login(request, user)
            request.session['loginUser'] = user

            # 登陆成功之后跳转到首页
            next_url = request.GET.get("next", reverse("users:index"))
            # 跳转到next_url
            response = redirect(next_url)
            # 判断是否记住用户名
            remember = request.POST.get("remember")
            if remember == "on":
                # 记住用户名
                response.set_cookie("username", username, max_age=7 * 24 * 3600)
            else:
                response.delete_cookie("username")
            return response
            # return render(request, "users/static_base.html", {})
        else:
            # 用户名或者密码错误
            return render(request, "users/login.html", {"error": "账户或密码有误"})


def user_alter_info(request):
    u_id = request.user.id
    user = models.UserInfo.objects.get(id=request.user.id)
    if request.method == "GET":

        return render(request, "users/user_alter_info.html", {})
    else:
        header = request.FILES.get("header")
        age = request.POST["age"]
        gender = request.POST["gender"]
        phone = request.POST["phone"].strip()
        nickname = request.POST["nickname"].strip()
        address = request.POST["address"].strip()
        # user = request.session["loginUser"]
        user.headers = header
        user.age = age
        user.gender = gender
        user.phone = phone
        user.nickname = nickname
        user.address = address
        if phone == '' or address == '':
            return render(request, "users/user_alter_info.html", {"msg":"电话或地址不能为空！"})
        else:
            user.save()
            request.session["login_user"] = user
            print(user.headers)
            return render(request, "users/user_center_info.html", {})


# 用户中心-信息页
@login_required
def user_center_info(request):
    return render(request, "users/user_center_info.html", {})


@login_required
def logout(request):
    auth.logout(request)
    # 跳转首页
    return redirect(reverse("users:user_login"))


# 修改密码

@login_required
def set_password(request):
    user = request.user
    if request.method == 'GET':
        return render(request, "users/set_password.html", {})
    elif request.method == 'POST':
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        repeat_password = request.POST.get("repeat_password")
        if user.check_password(old_password):  # 检查密码是否正确
            if not new_password:
                return render(request, 'users/set_password.html', {"msg": "新密码不能为空!"})

            elif new_password != repeat_password:
                return render(request, 'users/set_password.html', {"msg": "两次密码不一致!"})

            else:
                user.password = hashers.make_password(new_password)  # 正式修改密码，自动加密
                user.save()
                return redirect("users:index")
        else:
            return render(request, 'users/set_password.html', {"msg":"原密码输入错误"})


def watch(request):
    return render(request, "users/watch.html", {})


def add_address(request):
    if request.method == "GET":
        return render(request, "users/add_address.html", {})
    else:
        recv_name = request.POST["recv_name"]
        recv_tel = request.POST["recv_tel"]
        province = request.POST["province"]
        city = request.POST["city"]
        area = request.POST["area"]
        street = request.POST["street"]
        desc = request.POST["desc"]

        try:
            # 这个地址设为默认
            request.POST["status"]
            addresses = models.Address.objects.filter(user=request.user)

            for address in addresses:
                address.is_default = False
                address.save()
            address = models.Address(recv_name=recv_name, recv_tel=recv_tel,
                           province=province,
                           city=city,
                           area=area,
                           street=street,
                           desc=desc,
                           user=request.user,
                           status=True)
            address.save()
        except:
            address = models.Address(recv_name=recv_name, recv_tel=recv_tel,
                                     province=province,
                                     city=city,
                                     area=area,
                                     street=street,
                                     desc=desc,
                                     user=request.user,
                                     status=True)
            address.save()
        return redirect(reverse("users:address_list"))


def address_list(request):
    addresses = models.Address.objects.filter(user=request.user)
    return render(request, "users/address_list.html", {"addresses":addresses})
