# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from rest_framework import routers

from api.v1.base import admin_views as v1_admin_views
from api.v1.consumable import admin_views as v1_consumable_views


v1_admin_router = routers.DefaultRouter()
# base
v1_admin_router.register(r'auths', v1_admin_views.UserAuthViewSet, 'auths')
v1_admin_router.register(r'organizations', v1_admin_views.OrganizationViewSet, 'organization')
v1_admin_router.register(r'register', v1_admin_views.UserRegisterViewSet, 'register')
v1_admin_router.register(r'users', v1_admin_views.UserViewSet, 'users')
v1_admin_router.register(r'storagesites', v1_admin_views.StorageSitesViewSet, 'storagesites')
v1_admin_router.register(r'laboratories', v1_admin_views.LaboratoryViewSet, 'laboratories')
v1_admin_router.register(r'approves', v1_admin_views.ApproveViewSet, 'approves')

# consumable
v1_admin_router.register(r'suppliers', v1_consumable_views.SupplierViewSet, 'suppliers')
v1_admin_router.register(r'classifications', v1_consumable_views.ClassificationViewSet, 'classifications')
v1_admin_router.register(r'consumables', v1_consumable_views.ConsumableViewSet, 'consumables')
v1_admin_router.register(r'stocks', v1_consumable_views.StockViewSet, 'stocks')
v1_admin_router.register(r'picks', v1_consumable_views.PickViewSet, 'picks')
v1_admin_router.register(r'picklist', v1_consumable_views.PickListViewSet, 'picklist')

urlpatterns = [
    url(r'v1/', include([
        url(r'^admin/', include(v1_admin_router.urls)),
    ]))
]
