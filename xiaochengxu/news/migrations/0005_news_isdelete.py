# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-07-05 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20190703_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='isdelete',
            field=models.BooleanField(default=0),
        ),
    ]
