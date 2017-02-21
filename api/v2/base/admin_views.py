# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.db.models import (Q, When, Case, Count, Prefetch)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import (viewsets, status, serializers, validators)
from rest_framework.decorators import (list_route, detail_route)
from rest_framework.response import Response
from core.utils.pagination import NormalPagination
from base.models import Organization, User, Lab, StorageSites, Approve
from api.v1.base.admin_serializers import (OrganizationSerializer, UserAuthSerializer, UserRegisterSerializer,
                                           UserSerizalizer, StorageSitesSerializer, LaboratorySerializer, ApproveSerializer)

from api.v1.utils.viewsets import CsrfExemptViewSet, UserRequireViewSet
from api.v1.utils.caches import cache_for_admin_login, cache_for_admin_logout
from core.exceptions import BusinessValidationError
from api import error_const


class OrganizationViewSet(UserRequireViewSet):

    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    @list_route(methods=['get'], authentication_classes=[])
    def type_name(self, request):
        return Response(Organization.get_type_name())

    # @list_route(methods=['get'], authentication_classes=[])
    # def role_name(self, request):
    #     return Response(Role.get_role_name())

    def get_queryset(self):
        return Organization.objects.filter(id=self.request.real_company.id)


class UserRegisterViewSet(viewsets.ModelViewSet):

    serializer_class = UserRegisterSerializer
    queryset = Organization.objects.all()

    # def get_queryset(self):
    #     return self.queryset


class UserAuthViewSet(CsrfExemptViewSet):

    @list_route(methods=['post'])
    def login(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        try:
            ca = User.login(username, password)
            serializer = UserAuthSerializer(ca)
            cache_for_admin_login(serializer)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise BusinessValidationError(error_const.BUSINESS_ERROR.ADMIN_LOGIN_FAIL)


class UserViewSet(UserRequireViewSet):

    serializer_class = UserSerizalizer
    queryset = User.objects.all()
    search_fields = ('username', 'phone',)

    def get_queryset(self):
        return User.objects.filter(organization=self.request.real_company)


class StorageSitesViewSet(UserRequireViewSet):

    serializer_class = StorageSitesSerializer
    queryset = StorageSites.objects.all()

    def get_queryset(self):
        return StorageSites.objects.filter(organization=self.request.real_company)


class LaboratoryViewSet(UserRequireViewSet):
    serializer_class = LaboratorySerializer
    queryset = StorageSites.objects.all()

    def get_queryset(self):
        return Laboratory.objects.filter(organization=self.request.real_company)


class ApproveViewSet(UserRequireViewSet):
    serializer_class = ApproveSerializer
    queryset = Approve.objects.all()

    def get_queryset(self):
        return Approve.objects.filter(organization=self.request.real_company)