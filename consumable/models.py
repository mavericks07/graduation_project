from django.db import models
from core.models import Core
from base.models import Organization, StorageSites, Laboratory, User


class Supplier(Core):

    name = models.CharField('供应商名称', max_length=256)
    email = models.EmailField('邮箱')
    contacts = models.CharField('联系人', max_length=32)
    phone = models.CharField('联系电话', max_length=32)
    location = models.CharField('地址', max_length=256, null=True, blank=True)
    remark = models.CharField('备注', max_length=128, null=True, blank=True)
    organization = models.ForeignKey(Organization)

    common_fields = ('name', 'email', 'contacts', 'phone', 'location', 'remark') + Core.common_fields


class Classification(Core):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.name

    common_fields = ('name',) + Core.common_fields


class Consumable(Core):

    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=128)
    article_number = models.CharField(max_length=128)
    unit = models.CharField(max_length=16)
    classification = models.ForeignKey(Classification)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.name

    common_fields = ('name', 'brand', 'article_number', 'unit')


class Order(Core):
    consumables = models.ManyToManyField(Consumable, through='OrderConsumables')
    organization = models.ForeignKey(Organization)


class OrderConsumables(Core):
    consumable = models.ForeignKey(Consumable)
    order = models.ForeignKey(Order)
    quantity = models.FloatField()

    common_fields = ('quantity',)


class Stock(Core):

    consumable = models.ForeignKey(Consumable)
    number = models.IntegerField(default=0)
    storagesite = models.ForeignKey(StorageSites)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    organization = models.ForeignKey(Organization)

    common_fields = ('number',) + Core.common_fields


class PickList(Core):
    APPROVE_STATUS_PASS = 0
    APPROVE_STATUS_NOT_PASS = 1
    APPROVE_STATUS_ING = 2
    APPROVE_STATUS_REJECT = 3

    APPROVE_STATUS_CHOICE = (
        (APPROVE_STATUS_PASS, '通过'),
        (APPROVE_STATUS_NOT_PASS, u'未通过 '),
    )
    user = models.ForeignKey(User)
    status = models.IntegerField(choices=APPROVE_STATUS_CHOICE, default=APPROVE_STATUS_NOT_PASS)


class Pick(Core):

    stock = models.ForeignKey(Stock)
    number = models.IntegerField()
    lab = models.ForeignKey(Laboratory)
    list = models.ForeignKey(PickList)

    common_fields = ('number', ) + Core.common_fields




