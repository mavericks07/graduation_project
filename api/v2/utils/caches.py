# -*- coding: utf-8 -*-
from django.core.cache import cache


class CacheConst:
    User = 'USer'

    ID_KEY = "%s:ID:%s"
    TOKEN_KEY = "%s:TOKEN:%s"
    TOKEN_USER_KEY = "%s:TOKEN:USER:%s"
    TOKEN_ORGANIZATION_KEY = "%s:TOKEN:ORGANIZATION:%s"


def cache_for_login(KEY, result):
    ID_KEY, TOKEN_KEY, TOKEN_USER_KEY, TOKEN_ORGANIZATION_KEY = get_login_keys(KEY, result.data)
    old_login_user = cache.get(ID_KEY)
    if old_login_user is not None:
        cache_for_logout(KEY, old_login_user)

    cache.set(ID_KEY, result.data, timeout=60*60*24*2)
    cache.set(TOKEN_KEY, result.data, timeout=60*60*24*2)
    cache.set(TOKEN_USER_KEY, result.instance, timeout=None)
    cache.set(TOKEN_ORGANIZATION_KEY, result.instance.organization, timeout=None)


def cache_for_admin_login(result):
    cache_for_login(CacheConst.User, result)


def cache_for_admin_logout(data):
    cache_for_logout(CacheConst.User, data)


def cache_for_logout(KEY, data):
    ID_KEY, TOKEN_KEY, TOKEN_USER_KEY, TOKEN_ORGANIZATION_KEY = get_login_keys(KEY, data)

    cache.delete_pattern(ID_KEY)
    cache.delete_pattern(TOKEN_KEY)
    cache.delete_pattern(TOKEN_USER_KEY)
    cache.delete_pattern(TOKEN_ORGANIZATION_KEY)


def get_login_keys(KEY, data):
    return (
        CacheConst.ID_KEY % (KEY, data.get("id")),
        CacheConst.TOKEN_KEY % (KEY, data.get("token")),
        CacheConst.TOKEN_USER_KEY % (KEY, data.get("token")),
        CacheConst.TOKEN_ORGANIZATION_KEY % (KEY, data.get("token"))
    )


def get_company_admin_login_cache(token):
    KEY = CacheConst.User
    return get_login_cache(KEY, token)


def get_login_cache(KEY, token):
    return (
        cache.get(CacheConst.TOKEN_KEY % (KEY, token)),
        cache.get(CacheConst.TOKEN_USER_KEY % (KEY, token)),
        cache.get(CacheConst.TOKEN_ORGANIZATION_KEY % (KEY, token)),
    )