# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-07-15 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiezi_id', models.IntegerField()),
                ('content', models.CharField(max_length=255)),
            ],
        ),
    ]