from django.contrib import admin

# Register your models here.
from activety.models import *


@admin.register(Activety)
class ActivetyAdmin(admin.ModelAdmin):
    list_display=('id', 'img','name','support','explain','endtime',
                  'joinnum','getprize_userid','getprize_nickname','isvote')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display=('activety', 'choose','show_activetyname')
    def show_activetyname(self,obj):
            listdata = '<div style="color: blue;margin-top:2px">{}</div>'.format(obj.activety.name)
            return listdata
    show_activetyname.short_description = "活动名"
    show_activetyname.allow_tags = True

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display=('id', 'name','num','img','time','type')