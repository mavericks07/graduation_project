# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-30 18:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20161127_0315'),
        ('consumable', '0012_auto_20161201_0211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField(default=0)),
                ('consumable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumable.Consumable')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Organization')),
                ('storagesite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.StorageSites')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='consumable.Supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
