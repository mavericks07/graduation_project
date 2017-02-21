# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import (Q, When, Case, Count, Prefetch)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import (viewsets, status, serializers, validators)
from rest_framework.decorators import (list_route, detail_route)
from rest_framework.response import Response
from core.utils.pagination import NormalPagination
from base.models import Organization, User, Lab, StorageSites, Approve
from consumable.models import Supplier, Classification, Consumable, Stock, PickList, Pick, OperationRecord
from api.v1.base.admin_serializers import (OrganizationSerializer, UserAuthSerializer, UserRegisterSerializer,
                                           UserSerizalizer, StorageSitesSerializer, LaboratorySerializer)
from api.v2.consumable.admin_serializers import (SupplierSerializer, ClassificationSerializer, ConsumableSerializer,
                                                 StockSerializer, PickSerializer, PicksSerializer, PickListSerializer,
                                                 PickListListSerializer)
from api.v2.utils.viewsets import CsrfExemptViewSet, UserRequireViewSet
from core.exceptions import BusinessValidationError
from api import error_const
from core.utils.rest_fields import CurrentCompanyDefault, CurrentUserDefault


class SupplierViewSet(UserRequireViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

    def get_queryset(self):
        return Supplier.objects.filter(organization=self.request.real_company)


class ClassificationViewSet(UserRequireViewSet):
    serializer_class = ClassificationSerializer
    queryset = Classification.objects.all()

    def get_queryset(self):
        return Classification.objects.filter(organization=self.request.real_company)


class ConsumableViewSet(UserRequireViewSet):
    serializer_class = ConsumableSerializer
    queryset = Consumable.objects.all()

    def get_queryset(self):
        return Consumable.objects.filter(organization=self.request.real_company)

    @detail_route(methods=['post'])
    def pick(self, request):
        number = request.data.get('number', None)
        lab = request.data.get('lab', None)


class StockViewSet(UserRequireViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    def get_queryset(self):
        return Stock.objects.filter(organization=self.request.real_company)

    @detail_route(methods=['patch'])
    def stock(self, request, pk=None):
        number = int(request.data.get('number', None))
        current_stock = self.get_object()
        current_stock.number += number
        current_stock.save()
        current_user = self.request.real_user
        OperationRecord.add_record(current_user, current_stock, OperationRecord.OPERATION_TYPE_STOCK, number)
        serializer = StockSerializer(current_stock)
        return Response(serializer.data)

    @detail_route(methods=['post', 'get'])
    def pick(self, request, pk=None):
        current_user = self.request.real_user
        stock = request.data.get('stock', None)
        number = int(request.data.get('number', None))
        lab = request.data.get('lab', None)
        stock = get_object_or_404(Stock, pk=stock)
        if int(number) > stock.number:
            raise BusinessValidationError(error_const.BUSINESS_ERROR.MORE_THAN_STOCK)
        picklist = PickList.objects.get_or_create(user=current_user, status=PickList.APPROVE_STATUS_NOT_PASS)[0]
        print(picklist)
        condition = {
            'stock': stock,
            'lab_id': lab,
            'number': number,
            'can_return_number': number,
            'list': picklist
        }
        stock.number -= number
        stock.save()
        pick = Pick.objects.create(**condition)
        serializer = PickSerializer(pick)
        return Response(serializer.data)

    @list_route(methods=['get', 'delete'])
    def picklist(self, request):
        current_user = self.request.real_user
        picklist = get_object_or_404(PickList, user=current_user, status=PickList.APPROVE_STATUS_NOT_PASS)
        picks = picklist.pick_set.all()
        if request.method == 'DELETE':
            for pick in picks:
                stock = pick.stock
                stock.number += pick.number
                stock.save()
            picklist.delete()
        for pick in picks:
            stock = pick.stock
            OperationRecord.add_record(current_user, stock, OperationRecord.OPERATION_TYPE_PICK, pick.number)
        picklist.delete()
        serializer = PicksSerializer(picks)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def application(self, request):
        current_user = self.request.real_user
        picklist = get_object_or_404(PickList, user=current_user, status=PickList.APPROVE_STATUS_NOT_PASS)
        picklist.status = PickList.APPROVE_STATUS_ING
        picklist.save()
        return Response({})

    @detail_route(methods=['post'])
    def return_(self, request, pk=None):
        stock = self.get_object()
        current_user = self.request.real_user
        number = int(request.data.get('number', None))
        stock.number += number
        stock.save()
        OperationRecord.add_record(current_user, stock, OperationRecord.OPERATION_TYPE_RETURN, number)
        return Response({})


class PickViewSet(UserRequireViewSet):

    serializer_class = PickSerializer
    queryset = Pick.objects.all()

    def get_queryset(self):
        return Pick.objects.filter(lab__organization=self.request.real_company)

    @detail_route(methods=['post'])
    def return_(self, request, pk=None):
        pick = self.get_object()
        current_user = self.request.real_user
        number = int(request.data.get('number', None))
        if number > pick.can_return_number:
            raise BusinessValidationError(error_const.BUSINESS_ERROR.MORE_THAN_CAN_RETURN)
        stock = pick.stock
        pick.return_number += number
        pick.can_return_number -= number
        pick.save()
        stock.number += number
        stock.save()
        OperationRecord.add_record(current_user, stock, OperationRecord.OPERATION_TYPE_RETURN, number)
        return Response({})


class PickListViewSet(UserRequireViewSet):

    serializer_class = PickListSerializer
    queryset = PickList.objects.all()

    def get_queryset(self):
        return PickList.objects.filter(user__organization=self.request.real_company)

    @list_route(methods=['get'])
    def myapprove(self, request):
        current_user = self.request.real_user
        apporve = get_object_or_404(Approve, user=current_user, type=Approve.APPROVE_TYPE_GET)
        queryset = PickList.objects.exclude(status=PickList.APPROVE_STATUS_NOT_PASS)
        serializer = PickListListSerializer(queryset)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def myapplication(self, request):
        current_user = self.request.real_user
        queryset = PickList.objects.filter(user=current_user)
        serializer = PickListListSerializer(queryset)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def detail(self, request, pk=None):
        picklist = self.get_object()
        picks = picklist.pick_set.all()
        serializer = PicksSerializer(picks)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def agree(self, request, pk=None):
        picklist = self.get_object()
        picklist.status = PickList.APPROVE_STATUS_PASS
        picklist.save()
        return Response({})


