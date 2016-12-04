# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-15 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20161116_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='type',
            field=models.IntegerField(choices=[(1, '学校'), (2, '企业单位'), (3, '科研院所'), (4, '医院')], default=1, max_length=64, verbose_name='类型'),
        ),
    ]