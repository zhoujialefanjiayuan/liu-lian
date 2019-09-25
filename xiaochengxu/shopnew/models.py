from django.db import models

# Create your models here.
class Zhoubian(models.Model):
    name = models.CharField(max_length=120,default='')
    price = models.DecimalField(decimal_places = 2,max_digits=7)
    postage =models.IntegerField(default=0)
    main_img = models.CharField(max_length=256,default='')
    img1 = models.CharField(max_length=256,default='')
    img2 = models.CharField(max_length=256,default='')
    img3 = models.CharField(max_length=256,default='')
    img4 = models.CharField(max_length=256,default='')
    img5 = models.CharField(max_length=256,default='')
    detail1 = models.CharField(max_length=256,default='')
    detail2 = models.CharField(max_length=256,default='')
    detail3 = models.CharField(max_length=256,default='')
    detail4 = models.CharField(max_length=256,default='')
    detail5 = models.CharField(max_length=256,default='')
    canuse_coupon =  models.CharField(max_length=10,default='')
    color = models.CharField(max_length=50, default='')
    size = models.CharField(max_length=50, default='')
    describtion = models.CharField(max_length=500, default='')
    storenum = models.IntegerField(default=100)
    isdelete = models.BooleanField(default=0)

class Coupon(models.Model):
    require = models.IntegerField()
    reduce = models.IntegerField()

# type7种状态：1、待支付，  2、已支付待收货,21未揽件，22已揽件， 3、已收货（31满七天交易已完成，32未满七天可退款） 4、退货（41退货中；42退货失败；43退货成功）
#waitpay,waitget,canback,end
class Zhoubianorders(models.Model):
    order_num = models.CharField(max_length=50,unique=True,verbose_name='订单号')
    userid = models.CharField(max_length=500,verbose_name='用户id',default='orMHc4jj3K6-IZUu7DUMN8hVzwWw584')
    order_start_time = models.CharField(max_length=50,verbose_name='下单时间')
    pay_time = models.CharField(max_length=50,default='',verbose_name='支付时间')
    order_true_pay = models.DecimalField(decimal_places = 2,max_digits=7,verbose_name='实付金额') #实付
    receivetime = models.CharField(max_length=50,default='',verbose_name='收货时间')
    location_id = models.IntegerField(default=0)
    postage_fee = models.IntegerField(default=0)
    coupon_reduce = models.IntegerField(default=0)
    waybill_id = models.CharField(max_length=150,default='') #生成的运单ID
    logistics = models.CharField(max_length=10240,default='') #物流信息
    note_cont = models.CharField(max_length=500,default='') #留言信息
    ispay = models.BooleanField(default=0)
    isdelete = models.BooleanField(default=0)
    type = models.IntegerField(default=0,verbose_name='订单状态')

class Zhoubianorder_detail(models.Model):
    goodid = models.IntegerField(default=0)  # 商品id
    goodnum = models.IntegerField(default=0)  # 商品数量
    goodname = models.CharField(max_length=100)
    goodimg = models.CharField(max_length=500)
    goodprice = models.DecimalField(decimal_places=2, max_digits=7)
    orderForeignKey = models.ForeignKey(Zhoubianorders,default=1)

class Locationnote(models.Model):
    # consignee: this.username,
    # mobile: this.userPhone,
    # address: this.userAddress + this.detailAddress,
    # isdefult: this.isDefult,
    # region: this.region,
    # userAddress: this.userAddress,
    # detailAddress: this.detailAddress
    consignee =  models.CharField(max_length=50)
    mobile =  models.CharField(max_length=50)
    isdefult = models.BooleanField()
    region = models.CharField(max_length=500)
    detailaddress =  models.CharField(max_length=500)
    userid = models.CharField(max_length=300)
    isdelete = models.BooleanField(default=0)

class Car(models.Model):
    userid = models.CharField(max_length=150)
    goodid = models.IntegerField()
    num = models.IntegerField()
    isdelete = models.BooleanField(default=0)
    class Meta:
        unique_together = ('userid', 'goodid',)

class Topimg(models.Model):
    type = models.CharField(max_length=300)
    img = models.CharField(max_length=300)