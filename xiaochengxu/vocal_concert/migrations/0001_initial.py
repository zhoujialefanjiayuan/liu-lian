# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-05-17 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vocal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50)),
                ('project_connect', models.TextField(max_length=1024)),
                ('little_img', models.CharField(default=1, max_length=100)),
                ('img1', models.CharField(default=1, max_length=100)),
                ('img2', models.CharField(default=1, max_length=100)),
                ('img3', models.CharField(default=1, max_length=100)),
                ('img4', models.CharField(default=1, max_length=100)),
                ('img5', models.CharField(default=1, max_length=100)),
                ('singger', models.CharField(max_length=60)),
                ('city', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=30)),
                ('time', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vocal_swiper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50)),
                ('project_connect', models.TextField(max_length=1024)),
                ('little_img', models.CharField(default=1, max_length=100)),
                ('img1', models.CharField(default=1, max_length=100)),
                ('img2', models.CharField(default=1, max_length=100)),
                ('img3', models.CharField(default=1, max_length=100)),
                ('img4', models.CharField(default=1, max_length=100)),
                ('img5', models.CharField(default=1, max_length=100)),
                ('singger', models.CharField(max_length=60)),
                ('city', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=30)),
                ('time', models.CharField(max_length=50)),
            ],
        ),
    ]
