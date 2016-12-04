#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import OrderedDict
from rest_framework import (pagination)
from rest_framework.response import Response

class NormalPagination(pagination.PageNumberPagination):

    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('num_pages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
    
