# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-06-21 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0013_zhoubianorders_waybill_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zhoubianorders',
            name='receivetime',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='zhoubianorders',
            name='waybill_id',
            field=models.CharField(default='', max_length=150),
        ),
    ]