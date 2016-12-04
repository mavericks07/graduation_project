#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.exceptions import ValidationError


class BusinessValidationError(ValidationError):

    def __init__(self, detail):
        self.detail = {
            "code":detail[0],
            "msg":detail[1]
        }
        super(BusinessValidationError, self).__init__(self.detail)

BLANK_ERROR = {'blank': "该字段不能为空"}
