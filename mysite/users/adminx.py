

import xadmin
from django.contrib.auth.models import User
from . import models
from xadmin import views


xadmin.site.register(models.UserInfo)
xadmin.site.register(models.Address)

