# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-07-02 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0019_auto_20190701_1544'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='xianchangorder',
            options={'verbose_name_plural': '现场服务配送系统'},
        ),
        migrations.AlterModelOptions(
            name='zhoubianorders',
            options={'verbose_name_plural': '订单退款管理'},
        ),
        migrations.AddField(
            model_name='xianchangorder',
            name='order_senderman',
            field=models.CharField(default='', max_length=50, verbose_name='配送人'),
        ),
        migrations.AlterField(
            model_name='xianchangorder',
            name='isget',
            field=models.BooleanField(default=0, verbose_name='是否送达'),
        ),
        migrations.AlterField(
            model_name='xianchangorder',
            name='location_seat',
            field=models.CharField(max_length=512, verbose_name='座位地址'),
        ),
        migrations.AlterField(
            model_name='xianchangorder',
            name='location_site',
            field=models.CharField(max_length=512, verbose_name='场馆地址'),
        ),
        migrations.AlterField(
            model_name='xianchangorder',
            name='order_getman',
            field=models.CharField(max_length=50, verbose_name='收货人'),
        ),
        migrations.AlterField(
            model_name='xianchangorder',
            name='order_num',
            field=models.CharField(max_length=50, unique=True, verbose_name='订单号'),
        ),
        migrations.AlterField(
            model_name='xianchangorder',
            name='order_start_time',
            field=models.CharField(max_length=50, verbose_name='下单时间'),
        ),
        migrations.AlterField(
            model_name='xianchangorder',
            name='order_true_pay',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='付款金额'),
        ),
        migrations.AlterField(
            model_name='xianchangorder',
            name='phone',
            field=models.CharField(max_length=50, verbose_name='手机号'),
        ),
    ]