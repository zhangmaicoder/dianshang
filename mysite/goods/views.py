from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from . import models
from django.views.decorators.http import require_GET
from django.core.serializers import serialize
from store.models import Store


def add(request):
    if request.method == "GET":
        return render(request, "goods/add.html", {})
    else:
        name = request.POST["name"]
        price = request.POST["price"]
        stock = request.POST["stock"]
        store_id = request.POST["store"]
        type2 = request.POST["type2"]
        intro = request.POST["intro"]
        cover = request.FILES["cover"]

        store = Store.objects.get(pk=store_id)
        goodstype = models.GoodsType.objects.get(pk=type2)

        goods = models.Goods(name=name, price=price, stock=stock,intro=intro,stores=store,goodsType=goodstype)

        goods.save()
        goodsImage = models.GoodsImage(path=cover, goods=goods)
        goodsImage.save()
        return redirect(reverse("store:detail", kwargs={ "s_id": store_id}))


@require_GET
def findTypeByPId(request):
    parent__id = request.GET["parent__id"]
    type2s = models.GoodsType.objects.filter(parent=parent__id)

    return HttpResponse(serialize("json", type2s))


@require_GET
def detail(request, g_id):
    goods = models.Goods.objects.get(pk=g_id)
    return render(request, "goods./detail.html", {"goods": goods})



