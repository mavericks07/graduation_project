# -*- coding: utf-8 -*-
import binascii
import os
import math


def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()


def get_ip(request):
    ip = None
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


def split_array(arr, per_arr_size):
    split_arr = []
    size = len(arr)
    cnt = int(math.ceil(size/float(per_arr_size)))

    for i in range(cnt):
        if i+1 == cnt:
            split_arr.append(arr[i*per_arr_size:])
        else:
            split_arr.append(arr[i*per_arr_size:(i+1)*per_arr_size])
    return split_arr