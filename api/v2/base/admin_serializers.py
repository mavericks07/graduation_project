# -*- coding: utf-8 -*-
from rest_framework import serializers, validators
from core.utils import generate_token
from core.exceptions import BLANK_ERROR
from base.models import Organization, User, StorageSites, Lab, Approve
from core.utils.rest_fields import CurrentCompanyDefault
from core.exceptions import BusinessValidationError
from api import error_const


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = Organization.common_fields


# class RoleSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Role
#         fields = ('role_id',)


class UserSerizalizer(serializers.ModelSerializer):

    organization = serializers.HiddenField(default=CurrentCompanyDefault())
    role = serializers.IntegerField(default=1)
    password = serializers.CharField(default='123')

    class Meta:
        model = User
        fields = User.common_fields + ('role', 'organization',)

    def validate(self, attrs):
        print(attrs['username'])
        print(attrs)
        # if not attrs['role']:
        #     raise BusinessValidationError(error_const.BUSINESS_ERROR.STAFF_NOT_EXIST)
        # print(attrs['role'])
        return attrs

    def create(self, validated_data):
        role_id = validated_data.pop('role')
        print(role_id)
        # role = Role.objects.get(role_id=role_id)
        user = User.objects.create(**validated_data)
        # user.role.add(role)
        # for index, role_data in enumerate(roles_data):
        #     role = Role.objects.filter(**role_data).first()
        #     print(role_data['role_id'])
        #     user.role.add(role)
        # user.save()
        return user


class UserAuthSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    organization_vo = OrganizationSerializer(source='organization')

    class Meta:
        model = User
        fields = User.common_fields + ('organization_vo', 'token',)

    def get_token(self, admin):
        return generate_token()


class UserRegisterSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(UserRegisterSerializer, self).__init__(*args, **kwargs)  # call the super()
        for field in self.fields:  # iterate over the serializer fields
            self.fields[field].error_messages['blank'] = '*此项为必填'  # set the custom error message

    username = serializers.EmailField(error_messages={'invalid': '*请输入正确的邮箱格式'})
    password2 = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField()

    class Meta:
        model = User
        fields = User.common_fields + ('name', 'type', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次输入密码不一致')
        return attrs

    def create(self, validated_data):
        name = validated_data.pop('name', None)
        type = validated_data.pop('type', None)
        validated_data.pop('password2')
        organization = self.create_organization(name, type)
        user = User.objects.create(**validated_data)
        #role = Role.objects.filter(role_id=0).first()
        #user.role.add(role)
        user.organization = organization
        user.save()
        return user

    def create_organization(self, name, type):
        condition = {
            'name': name,
            'type': int(type)
        }
        organiztion = Organization.objects.create(**condition)
        organiztion.save()
        return organiztion


class StorageSitesSerializer(serializers.ModelSerializer):

    organization = serializers.HiddenField(default=CurrentCompanyDefault())

    class Meta:
        model = StorageSites
        fields = StorageSites.common_fields + ('organization',)


class LaboratorySerializer(serializers.ModelSerializer):

    organization = serializers.HiddenField(default=CurrentCompanyDefault())

    class Meta:
        model = Lab
        fields = Lab.common_fields + ('organization',)


class ApproveSerializer(serializers.ModelSerializer):

    organization = serializers.HiddenField(default=CurrentCompanyDefault())
    user_vo = UserSerizalizer(read_only=True, source='user')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Approve
        fields = Approve.common_fields + ('user_vo', 'organization', 'user')

    # def create(self, validated_data):
    #     user_id =
