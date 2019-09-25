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
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=150)),
                ('goodid', models.IntegerField()),
                ('num', models.IntegerField()),
                ('isdelete', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('require', models.IntegerField()),
                ('reduce', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Locationnote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consignee', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=50)),
                ('isdefult', models.BooleanField()),
                ('region', models.CharField(max_length=500)),
                ('detailaddress', models.CharField(max_length=500)),
                ('userid', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Zhoubian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=120)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('postage', models.IntegerField(default=0)),
                ('main_img', models.CharField(default='', max_length=256)),
                ('img1', models.CharField(default='', max_length=256)),
                ('img2', models.CharField(default='', max_length=256)),
                ('img3', models.CharField(default='', max_length=256)),
                ('img4', models.CharField(default='', max_length=256)),
                ('img5', models.CharField(default='', max_length=256)),
                ('detail1', models.CharField(default='', max_length=256)),
                ('detail2', models.CharField(default='', max_length=256)),
                ('detail3', models.CharField(default='', max_length=256)),
                ('detail4', models.CharField(default='', max_length=256)),
                ('detail5', models.CharField(default='', max_length=256)),
                ('canuse_coupon', models.CharField(default='', max_length=10)),
                ('color', models.CharField(default='', max_length=50)),
                ('size', models.CharField(default='', max_length=50)),
                ('storenum', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Zhoubianorder_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodid', models.IntegerField(default=0)),
                ('goodnum', models.IntegerField(default=0)),
                ('goodname', models.CharField(max_length=100)),
                ('goodimg', models.CharField(max_length=500)),
                ('goodprice', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Zhoubianorders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=50, unique=True, verbose_name='订单号')),
                ('userid', models.CharField(default='orMHc4jj3K6-IZUu7DUMN8hVzwWw584', max_length=500, verbose_name='用户id')),
                ('order_start_time', models.CharField(max_length=50, verbose_name='下单时间')),
                ('pay_time', models.CharField(default='', max_length=50, verbose_name='支付时间')),
                ('order_true_pay', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='实付金额')),
                ('receivetime', models.CharField(default='', max_length=50, verbose_name='收货时间')),
                ('location_id', models.IntegerField(default=0)),
                ('postage_fee', models.IntegerField(default=0)),
                ('coupon_reduce', models.IntegerField(default=0)),
                ('waybill_id', models.CharField(default='', max_length=150)),
                ('logistics', models.CharField(default='', max_length=10240)),
                ('note_cont', models.CharField(default='', max_length=500)),
                ('ispay', models.BooleanField(default=0)),
                ('isdelete', models.BooleanField(default=0)),
                ('type', models.IntegerField(default=0, verbose_name='订单状态')),
            ],
        ),
        migrations.AddField(
            model_name='zhoubianorder_detail',
            name='orderForeignKey',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shopnew.Zhoubianorders'),
        ),
        migrations.AlterUniqueTogether(
            name='car',
            unique_together=set([('userid', 'goodid')]),
        ),
    ]
