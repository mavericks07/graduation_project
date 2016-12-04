# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^buy$', views.buy, name='buy'),
    url(r'^consumable$', views.consumble, name='consumable'),
    url(r'^self$', views.self, name='self')
]
