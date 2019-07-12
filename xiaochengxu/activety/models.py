import datetime

from django.db import models

# Create your models here.
from paly.models import User
t = datetime.datetime.now()

class Activety(models.Model):
    img = models.CharField(max_length=255,verbose_name='活动海报')
    name = models.CharField(max_length=255,verbose_name='活动名')
    support = models.CharField(max_length=255,verbose_name='支持商')
    explain = models.CharField(max_length=1024,verbose_name='活动说明')
    endtime = models.DateTimeField(auto_now_add=True,verbose_name='活动截止时间')
    joinnum = models.IntegerField(default=0,verbose_name='参与人数')
    isvote = models.BooleanField(default=0,verbose_name='是否有投票')
    getprize_userid = models.CharField(max_length=255,default=None,verbose_name='获奖人id')
    getprize_nickname = models.CharField(max_length=255,default=None,verbose_name='获奖人昵称')
    class Meta:
        verbose_name_plural = '活动配置'


class Join(models.Model):
    activety = models.ForeignKey(Activety)
    userid =  models.CharField(max_length=255,default='')
    username =  models.CharField(max_length=255,default='')
    time = models.DateField(auto_now_add=True)


#优惠券 type:  1、周边，无门槛； 2、现场服务，无门槛
class Coupon(models.Model):
    name = models.CharField(max_length=255,default='',verbose_name='优惠券使用说明')
    num = models.DecimalField(max_digits=7,decimal_places=2,verbose_name='优惠金额')
    img = models.CharField(max_length=255,default='',verbose_name='优惠券图片')
    time = models.DateField(auto_now_add=True,verbose_name='过期时间')
    type = models.IntegerField(default=0,verbose_name='周边产品为1，现场服务为2')
    class Meta:
        verbose_name_plural = '优惠券配置'

class Usercoupon(models.Model):
    userid = models.CharField(max_length=255,default='')
    coupon  = models.ForeignKey(Coupon)

#投票功能选项
class Vote(models.Model):
    activety = models.ForeignKey(Activety,verbose_name='活动id')
    choose = models.CharField(max_length=255,verbose_name='选项名')
    num = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = '投票活动投票选项'
