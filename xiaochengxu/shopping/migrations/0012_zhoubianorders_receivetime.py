# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-06-21 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0011_auto_20190620_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='zhoubianorders',
            name='receivetime',
            field=models.CharField(default=None, max_length=50),
        ),
    ]