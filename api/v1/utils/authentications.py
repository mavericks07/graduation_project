#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import authentication
from rest_framework import exceptions
from core.exceptions import BusinessValidationError
from api import error_const
from api.v1.utils.caches import get_company_admin_login_cache


class UserAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        tokens = [token for token in 
                  [request.META.get('HTTP_AUTHORIZATION'), 
                   request.data.get('authorization', None), 
                   request.query_params.get('authorization',None)] 
                  if token is not None]
        if len(tokens) == 0:
            raise BusinessValidationError(error_const.COMMON_ERROR.AUTH_FAIL)

        user, real_user, real_company = get_company_admin_login_cache(tokens[0])

        if user:
            request.real_user = real_user
            request.real_company = real_company
            return (user, None)
        else:
            raise BusinessValidationError(error_const.COMMON_ERROR.AUTH_FAIL)


class CsrfExemptAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        return ({}, None)

