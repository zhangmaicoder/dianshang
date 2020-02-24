from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import login_required
from . import models
from django.views.decorators.http import require_GET
from goods.models import GoodsType,Goods


@login_required
def add(request):
    if request.method == "GET":
        return render(request, "store/add.html", {})
    else:
        name = request.POST["name"].strip()
        intro = request.POST["intro"].strip()
        print(name,intro)
        try:
            cover = request.FILES["cover"]
            store = models.Store(name=name, intro=intro, cover=cover,user=request.user)
        except:
            store = models.Store(name=name, intro=intro, user=request.user)
        store.save()
        return redirect(reverse("store:detail", kwargs={"s_id":store.id}))


@require_GET
@login_required
def list(request):
    stores = models.Store.objects.filter(user=request.user)
    return render(request, 'store/list.html', {"stores": stores})


@login_required
def update(request, s_id):
    if request.method == "GET":
        store = models.Store.objects.get(pk=s_id)
        return render(request, "store/update.html", {"store": store})
    else:
        name = request.POST["name"].strip()
        intro = request.POST["intro"].strip()

        store = models.Store.objects.get(pk=s_id)

        store.name = name
        store.intro = intro
        try:
            cover = request.FILES["cover"]
            store.cover = cover
        except:
            pass
        store.save()
        return redirect(reverse("store:detail", kwargs={"s_id":store.id}))


@require_GET
@login_required
def detail(request, s_id):
    store = models.Store.objects.get(pk=s_id)
    type1 = GoodsType.objects.filter(parent__isnull=True)
    goods = Goods.objects.filter(stores=store)

    return render(request, "store/detail.html", {"store": store, "goods": goods, "type1": type1})


@require_GET
def change(request, s_id, status):
    store = models.Store.objects.get(id=s_id)
    store.status = int(status)
    store.save()
    if store.status == 2:
        store.delete()
        return redirect(reverse("store:list"))
    else:
        return render(request, "store/detail.html", {"store": store})


def delete(request, s_id):
    pass




