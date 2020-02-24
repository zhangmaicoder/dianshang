from django.shortcuts import render,reverse,redirect
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from . import models
from goods.models import Goods


@require_GET
@login_required()
def add(request, count, goods_id):

    goods = Goods.objects.get(pk=goods_id)
    user = request.user

    try:
        cart = models.Cart.objects.get(user=user, goods=goods)
        cart.count += int(count)
        cart.allTotal = cart.count * goods.price
        cart.save()
    except Exception as e:
        print(e)
        cart = models.Cart(goods=goods, user=user)
        cart.count = int(count)
        cart.allTotal = cart.count * goods.price
        cart.save()
    return redirect(reverse("cart:list"))


def list(request):
    carts = models.Cart.objects.filter(user=request.user).order_by("-addTime")


    return render(request, "cart/list.html", {"carts": carts})


def delete(request,goods_id):

    try:
        goods = models.Cart.objects.filter(pk=goods_id)
        goods.delete()
        return render(request, "cart/delete.html", {})
    except Exception as e:
        print(e)


