from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^add/$", views.add, name='add'),
    url(r"^(?P<g_id>\d+)/detail/$", views.detail, name='detail'),
    url(r"^findTypeByPId/$", views.findTypeByPId, name='findTypeByPId'),
]
