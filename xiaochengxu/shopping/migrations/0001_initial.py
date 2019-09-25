# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-08-23 15:33
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
                ('goods_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.CharField(default='', max_length=512)),
                ('store_num', models.IntegerField()),
                ('picture1', models.CharField(default='', max_length=256)),
                ('picture2', models.CharField(default='', max_length=256)),
                ('picture3', models.CharField(default='', max_length=256)),
                ('picture4', models.CharField(default='', max_length=256)),
                ('picture5', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Locationforxianchang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=50, verbose_name='订单号')),
                ('refund_num', models.CharField(max_length=50, verbose_name='退款金额')),
                ('refund_time', models.DateTimeField(auto_now_add=True, verbose_name='退款时间')),
                ('refund_status', models.BooleanField(default=0, verbose_name='退款是否成功')),
            ],
            options={
                'verbose_name_plural': '退款单记录表',
            },
        ),
        migrations.CreateModel(
            name='Xianchangorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=50, verbose_name='订单号')),
                ('order_start_time', models.CharField(max_length=50, verbose_name='下单时间')),
                ('order_userid', models.CharField(max_length=256)),
                ('order_getman', models.CharField(max_length=50, verbose_name='收货人')),
                ('order_senderman', models.CharField(default='', max_length=50, verbose_name='配送人')),
                ('location_site', models.CharField(max_length=512, verbose_name='场馆地址')),
                ('location_seat', models.CharField(max_length=512, verbose_name='座位地址')),
                ('phone', models.CharField(max_length=50, verbose_name='手机号')),
                ('couponid', models.IntegerField(default=0)),
                ('order_true_pay', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='付款金额')),
                ('orderimg', models.CharField(default='http://liulian.szbeacon.com/%E8%BD%AE%E6%92%AD%E7%94%BB%E9%9D%A2_0002_%E7%BB%84-2-%E6%8B%B7%E8%B4%9D.png', max_length=150)),
                ('isget', models.BooleanField(default=0, verbose_name='是否送达')),
                ('ispay', models.BooleanField(default=0, verbose_name='是否支付')),
            ],
            options={
                'verbose_name_plural': '现场服务配送系统',
            },
        ),
        migrations.CreateModel(
            name='Xianchangorder_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodid', models.IntegerField(default=0)),
                ('goodnum', models.IntegerField(default=0)),
                ('goodname', models.CharField(max_length=100)),
                ('goodprice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('ordernum', models.CharField(default=0, max_length=50)),
                ('orderForeignKey', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shopping.Xianchangorder')),
            ],
        ),
        migrations.CreateModel(
            name='Zhoubian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=120)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
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
                ('order_num', models.CharField(max_length=50, unique=True, verbose_name='订单号')),
                ('order_start_time', models.CharField(max_length=50, verbose_name='下单时间')),
                ('order_user', models.CharField(max_length=256, verbose_name='收货用户ID')),
                ('order_location', models.CharField(max_length=512, verbose_name='收货地址')),
                ('order_phone', models.CharField(max_length=50, verbose_name='手机号')),
                ('couponid', models.IntegerField(default=0)),
                ('zhoubianid', models.IntegerField(default=0)),
                ('goodname', models.CharField(max_length=100, verbose_name='商品名')),
                ('goodimg', models.CharField(max_length=150)),
                ('goodprice', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='单价')),
                ('order_true_pay', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='实付金额')),
                ('goodnum', models.IntegerField(default=1, verbose_name='商品数量')),
                ('getman', models.CharField(default='qwert', max_length=50, verbose_name='收件人')),
                ('receivetime', models.CharField(default='', max_length=50, verbose_name='收货时间')),
                ('waybill_id', models.CharField(default='', max_length=150)),
                ('type', models.IntegerField(default=1, verbose_name='物流状态')),
            ],
            options={
                'verbose_name_plural': '订单退款管理',
            },
        ),
        migrations.AlterUniqueTogether(
            name='xianchangorder',
            unique_together=set([('order_num', 'order_senderman')]),
        ),
    ]
