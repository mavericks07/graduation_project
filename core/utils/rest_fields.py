#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import JSONField as RestJSONField
from rest_framework.serializers import Field
from rest_framework.exceptions import ValidationError
from rest_framework.compat import (unicode_to_repr)


class JSONField(RestJSONField):

    def to_representation(self, value):
        if self.binary:
            value = json.dumps(value)
            if isinstance(value, six.text_type):
                value = bytes(value.encode('utf-8'))
            return value
        else:
            if not value or len(value) == 0:
                value = '[]'
            if isinstance(value, six.text_type):
                _value = json.loads(value)
                return _value
                # return json.dumps(_value, ensure_ascii=False)
            else:
                return value

class DateStrField(Field):
    format = '%Y-%m-%d'

    def __init__(self, format=None, *args, **kwargs):
        self.format = format or self.format
        super(DateStrField, self).__init__(*args, **kwargs)

    def to_internal_value(self, value):
        datetime.strptime(value, self.format) 
        return value

    def to_representation(self, value):
        datetime.strptime(value, self.format) 
        return value


class CurrentCompanyDefault(object):
    def set_context(self, serializer_field):
        self.company = serializer_field.context['request'].real_company

    def __call__(self):
        return self.company

    def __repr__(self):
        return unicode_to_repr('%s()' % self.__class__.__name__)


class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].real_user

    def __call__(self):
        return self.user

    def __repr__(self):
        return unicode_to_repr('%s()' % self.__class__.__name__)


class TheSameCompanyValidator(object):
    """
    Validator that corresponds to `unique=True` on a model field.

    Should be applied to an individual field on the serializer.
    """
    message = _('数据有误，对象{field}的公司与登录用户公司不相同')

    def __init__(self, field, message=None):
        self.message = message or self.message
        self.field = field

    def __call__(self, attrs):
        target = None
        company = None
        for field, value in attrs.items():
            if field == self.field:
                target = value
            if field == 'company':
                company = value

        if target is not None and target.company != company:
            raise ValidationError(self.message.format(field=self.field))

    def __repr__(self):
        return unicode_to_repr('<%s>' % ( self.__class__.__name__))
