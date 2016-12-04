from django.db import models
from core.models import Core


class Organization(Core):

    TYPE_SCHOOL = 1
    TYPE_COMPANY = 2
    TYPE_SCIENTIFIC_RESEARCH_UNITS = 3
    TYPE_HOSPITAL = 4

    TYPE_CHOICE = (
        (TYPE_SCHOOL, '学校'),
        (TYPE_COMPANY, u'企业单位'),
        (TYPE_SCIENTIFIC_RESEARCH_UNITS, u'科研院所'),
        (TYPE_HOSPITAL, u'医院')
    )

    name = models.CharField(u'机构名称', max_length=128)
    location = models.CharField(u'地址', null=True, max_length=256)
    homepage = models.CharField(u'主页', null=True, max_length=128)
    type = models.IntegerField(u'类型', choices=TYPE_CHOICE, default=TYPE_SCHOOL)
    primary_service = models.CharField(u'主营业务', null=True, max_length=128)
    phone = models.CharField(u'电话', null=True, blank=True, max_length=12)

    common_fields = ('name', 'location', 'homepage', 'primary_service', 'type_name', 'phone', 'type') + Core.common_fields

    def __str__(self):
        return self.name

    @staticmethod
    def get_type_name():
        t = dict(Organization.TYPE_CHOICE)
        return t

    @property
    def type_name(self):
        return Organization.get_type_name()[self.type]

    class Meta:
        pass


class StorageSites(Core):

    name = models.CharField(u'存放地名称', max_length=128)
    remark = models.CharField(u'备注', max_length=256, null=True, blank=True)
    organization = models.ForeignKey(Organization, verbose_name=u'所属机构')

    common_fields = ('name', 'remark',) + Core.common_fields

    def __str__(self):
        return self.name


class Laboratory(Core):

    name = models.CharField(u'实验室名称', max_length=128)
    remark = models.CharField(u'备注', max_length=256, null=True, blank=True)
    organization = models.ForeignKey(Organization, verbose_name=u'所属机构')

    common_fields = ('name', 'remark',) + Core.common_fields


class Role(Core):

    ROLE_ADMIN = 0
    ROLE_LA = 1
    ROLE_BUYER = 2
    ROLE_APPROVER = 3
    ROLE_Warehouse_keeper = 4

    ROLE_CHOICE = (
        (ROLE_ADMIN, '系统管理员'),
        (ROLE_LA, '实验员'),
        (ROLE_BUYER, '采购员'),
        (ROLE_APPROVER, '审批人'),
        (ROLE_Warehouse_keeper, '库管员')
    )

    role_id = models.IntegerField(choices=ROLE_CHOICE, default=ROLE_LA)
    name = models.CharField(u'角色名称', max_length=128)

    @staticmethod
    def create_roles():
        roles = {
            0: '系统管理员',
            1: '实验员',
            2: '采购员',
            3: '审批人',
            4: '库管员'
        }
        for role_id in roles:
            id = Role.objects.filter(role_id=role_id).first()
            if id is None:
                role = Role(role_id=role_id,  name=roles[role_id])
                role.save()

    def __str__(self):
        return self.name

    @staticmethod
    def get_role_name():
        t = dict(Role.ROLE_CHOICE)
        return t


class User(Core):

    username = models.CharField(u'用户名', max_length=128)
    password = models.CharField(u'密码', max_length=128)
    phone = models.CharField(u'电话', max_length=12, null=True, blank=True)
    role = models.ManyToManyField(Role, verbose_name=u'所属角色')
    organization = models.ForeignKey(Organization, verbose_name=u'所属机构', null=True, blank=True)

    name = None
    type = None
    password2 = None

    common_fields = ('username', 'password', 'phone',) + Core.common_fields

    @staticmethod
    def login(username, password):
        return User.objects.get(username=username, password=password)

