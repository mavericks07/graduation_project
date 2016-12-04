# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-04 05:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20161127_0315'),
        ('consumable', '0013_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pick',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField()),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Laboratory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PickList',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(choices=[(0, '通过'), (1, '未通过 ')], default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='pick',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumable.PickList'),
        ),
        migrations.AddField(
            model_name='pick',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumable.Stock'),
        ),
    ]
