from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_POST
from cart.models import Cart
from users.models import Address
from goods.models import Goods
from . import models


@require_POST
def confirm(request):
    g_ids = request.POST.getlist("g_id")
    myCart = Cart.objects.filter(pk__in=g_ids)
    addresses = Address.objects.filter(user=request.user)
    return render(request, "orders/confirm.html", {"myCart": myCart, "addresses": addresses})


def pay(request):
    pass


@require_POST
def done(request):
    c_ids = request.POST.getlist("c_id")
    print(c_ids)
    address_id = request.POST["address"]

    address = Address.objects.get(pk=address_id)
    carts = Cart.objects.filter(pk__in=c_ids)

    _address = address.province+"|"+address.city+"|"+ address.area +"|"+address.street+"|"+address.desc
    # 生成订单
    order = models.Order(recv_address=_address, user=request.user, recv_name=address.recv_name,recv_tel=address.recv_tel, all_price=0, remark='')
    order.save()
    allCount = 0
    for s in carts:
        g = s.goods
        orderItem = models.OrderItem(id=g.id, goods_img=g.goodsimage_set.all().first().path,\
                         goods_name=g.name, goods_price=g.price, goods_count=s.count,
                         goods_price_all=s.allTotal,order=order)
        orderItem.save()
        allCount += s.allTotal
    order.all_price = allCount

    order.save()
    return redirect(reverse("orders:list"))


def list(request):
    orders = models.Order.objects.filter(user=request.user)
    return render(request, "orders/list.html", {"orders": orders})


def detail(request, o_id):
    pass


def delete(request, o_id):

    try:
        od = models.Order.objects.filter(pk=o_id)
        od.delete()
        return render(request, "orders/delete.html", {})
    except Exception as e:
        print(e)
