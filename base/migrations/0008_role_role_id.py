# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-22 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20161122_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='role_id',
            field=models.IntegerField(choices=[(0, '系统管理员'), (1, '实验员'), (2, '采购员'), (3, '审批人')], default=1),
        ),
    ]