from django.contrib import admin

# Register your models here.
from django.db.models import Q

from shopping.models import ZhouBianorders, Xianchangorder_detail
from shopping.models import Refund
from shopping.models import Xianchangorder


@admin.register(ZhouBianorders)
class ZhouBianordersAdmin(admin.ModelAdmin):
    list_display=('id', 'order_num', 'order_start_time', 'receivetime','order_user','getman','order_location','order_phone','goodname',
                  'goodprice','goodnum','order_true_pay','colored_type','refund','refuse')
    search_fields = ('order_num',)  # 搜索字段

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display=('id', 'order_num','refund_time','refund_status')
    search_fields = ('order_num',)  # 搜索字段

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

# hobby_set.all()

@admin.register(Xianchangorder)
class XianchangorderAdmin(admin.ModelAdmin):
    list_display=('id', 'order_num','location_site','location_seat','order_getman','phone',
                  'order_true_pay','show_all_goods','getorder','order_senderman','issended')

    ordering = ('order_senderman',)
    #只能获取未接单，和自身接单的数据
    def get_queryset(self, request):
        """函数作用：使当前登录的用户只能看到自己负责的服务器"""
        qs = super(XianchangorderAdmin, self).get_queryset(request)
        if request.user.username == 'zhou':
            return qs
        return qs.filter(Q(order_senderman=request.user.username)|Q(order_senderman=''))

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False


    #自定义接单操作
    actions = ['makesuregetorder','makesuresend']
    def makesuregetorder(self, request, queryset):
        for obj in queryset.filter():
            obj.order_senderman = request.user.username
            obj.save()
    makesuregetorder.short_description = "确认接单"


    def makesuresend(self, request, queryset):
        for obj in queryset.filter():
            obj.isget = 1
            obj.save()

    makesuresend.short_description = "商品已送达"

    def show_all_goods(self,obj):
        if obj.order_senderman != '':
            listdata = ['<div style="color: blue;margin-top:2px">{} X {}</div>'.format(a.goodname,a.goodnum) for a in obj.xianchangorder_detail_set.all()]
            return ''.join(listdata)
    show_all_goods.short_description = "订单详情"
    show_all_goods.allow_tags = True

