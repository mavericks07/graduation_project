# -*- coding: utf-8 -*-
from rest_framework import serializers, validators
from core.utils import generate_token
from core.exceptions import BLANK_ERROR
from base.models import Organization, User, Role, StorageSites, Laboratory
from consumable.models import Supplier, Classification, Consumable, Stock, Pick, PickList
from core.utils.rest_fields import CurrentCompanyDefault, CurrentUserDefault
from core.exceptions import BusinessValidationError
from api import error_const
from api.v1.base.admin_serializers import StorageSitesSerializer, LaboratorySerializer


class SupplierSerializer(serializers.ModelSerializer):

    organization = serializers.HiddenField(default=CurrentCompanyDefault())

    class Meta:
        model = Supplier
        fields = Supplier.common_fields + ('organization',)


class ClassificationSerializer(serializers.ModelSerializer):

    organization = serializers.HiddenField(default=CurrentCompanyDefault())

    class Meta:
        model = Classification
        fields = Classification.common_fields + ('organization',)


class ConsumableSerializer(serializers.ModelSerializer):

    organization = serializers.HiddenField(default=CurrentCompanyDefault())
    classification_vo = ClassificationSerializer(source='classification', read_only=True)
    classification = serializers.PrimaryKeyRelatedField(queryset=Classification.objects.all(), write_only=True)
    # number = serializers.IntegerField()
    # s = serializers.PrimaryKeyRelatedField(source='StorageSites', read_only=True)

    class Meta:
        model = Consumable
        fields = Consumable.common_fields + ('organization', 'classification', 'classification_vo')

    def create(self, validated_data):
        number = validated_data.pop('number')
        c = Consumable.objects.create(**validated_data)
        return c


class StockSerializer(serializers.ModelSerializer):

    # user = serializers.HiddenField(default=CurrentUserDefault())
    organization = serializers.HiddenField(default=CurrentCompanyDefault())
    consumable_vo = ConsumableSerializer(source='consumable', read_only=True)
    storagesite_vo = StorageSitesSerializer(source='storagesite', read_only=True)
    supplier_vo = SupplierSerializer(source='supplier', read_only=True, allow_null=True)
    consumable = ConsumableSerializer(write_only=True)
    storagesite = serializers.PrimaryKeyRelatedField(queryset=StorageSites.objects.all(), write_only=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False, write_only=True)

    class Meta:
        model = Stock
        fields = Stock.common_fields + ('organization', 'consumable_vo', 'storagesite_vo', 'consumable', 'storagesite',
                                        'supplier_vo', 'supplier',)

    def create(self, validated_data):
        print()
        consumable_data = validated_data.pop('consumable')
        consumable = Consumable.objects.create(**consumable_data)
        consumable.save()
        stock = Stock.objects.create(consumable=consumable, **validated_data)
        return stock


class PickSerializer(serializers.ModelSerializer):

    stock_vo = StockSerializer(source='stock', read_only=True)
    lab_vo = LaboratorySerializer(source='lab', read_only=True)
    list = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Pick
        fields = Pick.common_fields + ('stock_vo', 'lab_vo', 'list')


class PickListSerializer(serializers.ListSerializer):

    child = PickSerializer()







