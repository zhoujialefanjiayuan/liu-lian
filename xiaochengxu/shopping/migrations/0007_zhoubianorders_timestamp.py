# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-06-18 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0006_auto_20190618_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='zhoubianorders',
            name='timestamp',
            field=models.CharField(default='qwert', max_length=50),
        ),
    ]