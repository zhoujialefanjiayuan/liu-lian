from django.db import models

# Create your models here.
#现场商品表
from django.utils.html import format_html


class Goods(models.Model):
    type = models.IntegerField()
    goods_name = models.CharField(max_length=256)
    goods_price = models.DecimalField(decimal_places=2,max_digits=6)
    description = models.CharField(max_length= 512,default='')
    store_num = models.IntegerField()
    picture = models.CharField(max_length=256)

#商品类
class Good_types(models.Model):
    type_name = models.CharField(max_length=256)
    type_icon = models.CharField(max_length=256)


#周边商品
class Zhoubian(models.Model):
    name = models.CharField(max_length=120,default='')
    price = models.DecimalField(decimal_places = 2,max_digits=7)
    log = models.CharField(max_length=256,default='')
    img = models.CharField(max_length=256,default='')
    detail1 = models.CharField(max_length=256,default='')
    detail2 = models.CharField(max_length=256,default='')
    detail3 = models.CharField(max_length=256,default='')
    detail4 = models.CharField(max_length=256,default='')

#周边订单表
# type7种状态：1、待支付，  2、已支付待收货， 3、已收货（31满七天交易已完成，32未满七天可退款） 4、退货（41退货中；42退货失败；43退货成功）
class ZhouBianorders(models.Model):
    order_num = models.CharField(max_length=50,unique=True,verbose_name='订单号')
    order_start_time = models.CharField(max_length=50,verbose_name='下单时间')
    order_user = models.CharField(max_length=256,verbose_name='收货用户ID')
    order_location = models.CharField(max_length=512,verbose_name='收货地址')
    order_phone = models.CharField(max_length=50,verbose_name='手机号')
    couponid = models.IntegerField(default=0) #优惠券id
    zhoubianid = models.IntegerField(default=0) #周边id
    goodname = models.CharField(max_length=100,verbose_name='商品名')
    goodimg = models.CharField(max_length=150)
    goodprice = models.DecimalField(decimal_places = 2,max_digits=7,verbose_name='单价')
    order_true_pay = models.DecimalField(decimal_places = 2,max_digits=7,verbose_name='实付金额') #实付
    goodnum = models.IntegerField(default=1,verbose_name='商品数量')
    getman = models.CharField(max_length=50,default='qwert',verbose_name='收件人')
    receivetime = models.CharField(max_length=50,default='',verbose_name='收货时间')
    waybill_id = models.CharField(max_length=150,default='') #生成的运单ID
    type = models.IntegerField(default=1,verbose_name='物流状态')

    def colored_type(self):
        if self.type == 2:
            return format_html(
                '<span style="color: {};">{}</span>',"green","待收货"
            )
        elif self.type == 31:
            return format_html(
                '<span style="color: {};">{}</span>','black','交易完成'
            )
        elif self.type == 32:
            return format_html(
                '<span style="color: {};">{}</span>','red','可退款'
            )
        elif self.type == 41:
            return format_html(
                '<span style="color: {};">{}</span>','red','退货中，待收退货商品'
            )
        elif self.type == 42:
            return format_html(
                '<span style="color: {};">{}</span>','red','商品有损坏，退货失败'
            )
        else:
            return format_html(
                '<span style="color: {};">{}</span>','green','退款成功'
            )
    colored_type.short_description = '签收状态'

    def refund(self):
        """自定义一个a标签，跳转到实现复制数据功能的url"""
        if self.type == 41:
            url= 'http://101.132.47.14/shop/refundment/?order_num={}'.format(self.order_num)
            title = '允许退款'
            return '<a href="{}">{}</a>'.format(url, title)
    refund.short_description = '允许退款'
    refund.allow_tags = True

    def refuse(self):
        """自定义一个a标签，跳转到实现复制数据功能的url"""
        if self.type == 41:
            url= 'http://101.132.47.14/shop/refuse_return/?order_num={}'.format(self.order_num)
            title = '拒绝退款'
            return '<a href="{}">{}</a>'.format(url, title)
    refuse.short_description = '拒绝退款'
    refuse.allow_tags = True

    class Meta:
        verbose_name_plural = '订单退款管理'

#退款单表
class Refund(models.Model):
    order_num = models.CharField(max_length=50,verbose_name='订单号')
    refund_num = models.CharField(max_length=50,verbose_name='退款金额')
    refund_time = models.DateTimeField(auto_now_add=True,verbose_name='退款时间')
    refund_status = models.BooleanField(default=0,verbose_name='退款是否成功') #退款状态

    class Meta:
        verbose_name_plural = '退款单记录表'

#现场商品订单
class Xianchangorder(models.Model):
    order_num = models.CharField(max_length=50, unique=True,verbose_name='订单号')
    order_start_time = models.CharField(max_length=50,verbose_name='下单时间')
    order_userid = models.CharField(max_length=256)
    order_getman = models.CharField(max_length=50,verbose_name='收货人')
    order_senderman = models.CharField(max_length=50,default='',verbose_name='配送人')
    location_site = models.CharField(max_length=512,verbose_name='场馆地址')
    location_seat = models.CharField(max_length=512,verbose_name='座位地址')
    phone = models.CharField(max_length=50,verbose_name='手机号')
    couponid = models.IntegerField(default=0)  # 优惠券id
    order_true_pay = models.DecimalField(decimal_places=2, max_digits=7,verbose_name='付款金额')  # 实付
    orderimg = models.CharField(max_length=150,default='http://liulian.szbeacon.com/%E8%BD%AE%E6%92%AD%E7%94%BB%E9%9D%A2_0002_%E7%BB%84-2-%E6%8B%B7%E8%B4%9D.png')
    isget = models.BooleanField(default=0,verbose_name='是否送达')
    ispay = models.BooleanField(default=0,verbose_name='是否支付')
    class Meta:
        verbose_name_plural = '现场服务配送系统'
    #是否送达
    def issended(self):
        """自定义一个a标签，跳转到实现复制数据功能的url"""
        if self.isget == 0:
            return '<span style="color: red;">未送达</span>'
        else:
            return  '<span style="color: green;">已送达</span>'
    issended.short_description = '是否送达'
    issended.allow_tags = True

    # 接单
    def getorder(self):
        """自定义一个a标签，跳转到实现复制数据功能的url"""
        if self.order_senderman == '':
            return '<span style="color: red;">待接单</span>'
        else:
            return '<span style="color: green;">已接单</span>'

    getorder.short_description = '接单'
    getorder.allow_tags = True


class Xianchangorder_detail(models.Model):
    goodid = models.IntegerField(default=0)  # 商品id
    goodnum = models.IntegerField(default=0)  # 商品数量
    goodname = models.CharField(max_length=100)
    goodprice = models.DecimalField(decimal_places=2, max_digits=7)
    ordernum = models.CharField(max_length=50,default=0)
    orderForeignKey = models.ForeignKey(Xianchangorder,default=1)


