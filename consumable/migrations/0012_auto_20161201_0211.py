# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-30 18:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumable', '0011_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='consumable',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='storagesite',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='supplier',
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
    ]