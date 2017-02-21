# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from configurations import Configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseConfig(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BROKER_URL = 'redis://127.0.0.1:6379/8'

    SECRET_KEY = 'f94u4i2wwp&tdt8@-i4s71d=qdi#*_macg0&&e(fw5ne1_l%d7'
    DEBUG = True

    STATIC_URL = '/static/'

    ALLOWED_HOSTS = ['*']

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'base',
        'consumable',
    ]

    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'graduation_project.urls'

    WSGI_APPLICATION = 'graduation_project.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'lab',
            'USER': 'root',
            'PASSWORD': '123456',
            'HOST': '127.0.0.1',
            'PORT': '3306'
        },
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/9",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    REST_FRAMEWORK = {
        # 'DEFAULT_PAGINATION_CLASS': 'core.utils.pagination.NormalPagination',
        'PAGE_SIZE': 20,
        'EXCEPTION_HANDLER': 'core.views.exception_handler',
        'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
        'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
        'DATETIME_INPUT_FORMATS': ('%Y-%m-%d %H:%M:%S', )
    }

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'Asia/Shanghai'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

    STATICFILES_DIRS = (

        os.path.join(BASE_DIR, 'static/'),

    )
