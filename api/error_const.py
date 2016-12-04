#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class COMMON_ERROR():
    '''
        通用错误
    '''
    AUTH_FAIL = ("AUTH_FAIL","权限验证失败")
    EXISTS = ("OBJECT_EXISTS","对象已存在")
    VALID_FAIL = ("VALID_FAIL","参数验证失败")


class BUSINESS_ERROR():
    '''
        业务错误
    '''

    MORE_THAN_STOCK = ('MORE_THAN_STOCK', '领用数量大于库存')


