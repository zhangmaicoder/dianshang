from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^(?P<count>\d+)/(?P<goods_id>\d+)/add/$", views.add, name="add"),
    url(r"^list/$", views.list, name="list"),
    url(r"^(?P<goods_id>\d+)/delete/$", views.delete, name="delete"),
]


