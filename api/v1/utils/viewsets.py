#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import (viewsets, status, filters)
from api.v1.utils.authentications import (CsrfExemptAuthentication, UserAuthentication)


class CsrfExemptViewSet(viewsets.ViewSet):
    authentication_classes = (CsrfExemptAuthentication, )


class UserRequireViewSet(viewsets.ModelViewSet):
    authentication_classes = (UserAuthentication, )
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )






