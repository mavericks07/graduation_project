from django.db import models
from core.models import Core
from base.models import Organization, StorageSites, Lab, User


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
        (APPROVE_STATUS_ING, '审批中'),
        (APPROVE_STATUS_REJECT, '被驳回')
    )
    user = models.ForeignKey(User)
    status = models.IntegerField(choices=APPROVE_STATUS_CHOICE, default=APPROVE_STATUS_NOT_PASS)

    common_fields = ('status_name',) + Core.common_fields

    @property
    def status_name(self):
        return self.APPROVE_STATUS_CHOICE[self.status][1]


class Pick(Core):

    stock = models.ForeignKey(Stock)
    number = models.IntegerField()
    return_number = models.IntegerField(default=0)
    can_return_number = models.IntegerField()
    lab = models.ForeignKey(Lab)
    list = models.ForeignKey(PickList)

    common_fields = ('number', 'return_number', 'can_return_number',) + Core.common_fields

    def can_return(self):
        if self.return_number <= self.can_return_number:
            return True
        return False


class OperationRecord(Core):

    OPERATION_TYPE_STOCK = 0
    OPERATION_TYPE_PICK = 1
    OPERATION_TYPE_RETURN = 2
    OPERATION_TYPE_DELETE = 3

    OPERATION_TYPE_CHOICE = (
        (OPERATION_TYPE_STOCK, '入库'),
        (OPERATION_TYPE_PICK, '领用'),
        (OPERATION_TYPE_RETURN, '归还'),
        (OPERATION_TYPE_DELETE, '删除')
    )

    user = models.ForeignKey(User)
    type = models.IntegerField()
    stock = models.ForeignKey(Stock)
    number = models.IntegerField(null=True, blank=True)

    common_fields = ('type_name', 'number',) + Core.common_fields

    @property
    def type_name(self):
        return self.OPERATION_TYPE_CHOICE[self.type][1]

    @staticmethod
    def add_record(user, stock, type, number):
        create_op_record_condition = {
            'user': user,
            'stock': stock,
            'type': type,
            'number': number
        }
        op_record = OperationRecord.objects.create(**create_op_record_condition)
        op_record.save()






