# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-06-17 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Good_types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=256)),
                ('type_icon', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('goods_name', models.CharField(max_length=256)),
                ('goods_price', models.DecimalField(decimal_places=1, max_digits=6)),
                ('description', models.CharField(default='', max_length=512)),
                ('store_num', models.IntegerField()),
                ('picture', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Zhoubian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=120)),
                ('price', models.IntegerField(default=0)),
                ('log', models.CharField(default='', max_length=256)),
                ('img', models.CharField(default='', max_length=256)),
                ('detail1', models.CharField(default='', max_length=256)),
                ('detail2', models.CharField(default='', max_length=256)),
                ('detail3', models.CharField(default='', max_length=256)),
                ('detail4', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ZhouBianorders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=50, unique=True)),
                ('order_time', models.DateField(auto_now_add=True)),
                ('order_user', models.CharField(max_length=256)),
                ('order_location', models.CharField(max_length=512)),
                ('order_phone', models.CharField(max_length=50)),
                ('couponid', models.IntegerField(default=0)),
                ('order_true_pay', models.IntegerField()),
                ('type', models.IntegerField(default=1)),
                ('order_good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.Zhoubian')),
            ],
        ),
    ]