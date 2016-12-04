# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^login$', views.login, name='login'),
    url(r'^index$', views.index, name='index'),
    # url(r'^buy$', views.buy, name='buy'),
]