from django.shortcuts import render

# Create your views here.
from deliverysystem.models import *
from django.http import JsonResponse

from news.views import to_dict
from shopping.models import Xianchangorder


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = Userforsendor.objects.filter(username = username,password = password)
    if user.exists():
        return JsonResponse({'status':1,'userdata':{'username':user[0].username,'password':user[0].password,'token':user[0].token}})
    else:
        return JsonResponse({'status':0,'userdata':''})


def not_send(request):
    orders = Xianchangorder.objects.filter(ispay=1,order_senderman='').order_by('-order_start_time')
    orderlist = []
    for i in orders:
        obj = {}
        obj['id'] = i.id
        obj['order_num'] = i.order_num
        obj['order_start_time'] = i.order_start_time
        obj['location_seat'] =i.location_seat
        orderlist.append(obj)
    return JsonResponse({'status':1,'data':orderlist})

def getorder(request):
    token = request.POST.get('token')
    orderid = request.POST.get('orderid')
    order = Xianchangorder.objects.get(id = orderid)
    if order.order_senderman != '':
        return JsonResponse({'status':1})
    else:
        try:
            order.order_senderman = token
            order.save()
            return JsonResponse({'status': 1})
        except:
            return JsonResponse({'status':1})

def needsend(request):
    token = request.POST.get('token')
    needsend_order = Xianchangorder.objects.filter(order_senderman=token).order_by('isget')
    orderlist = []
    for i in needsend_order:
        obj = {}
        obj['id'] = i.id
        obj['order_num'] = i.order_num
        obj['order_start_time'] = i.order_start_time
        obj['location_seat'] = i.location_seat
        obj['isget'] = i.isget
        orderlist.append(obj)
    return JsonResponse({'status': 1, 'data': orderlist})


def orderdetail(request):
    orderid = int(request.GET.get('id'))
    order = Xianchangorder.objects.get(id = orderid)
    data = to_dict(order)
    goodsdetails = order.xianchangorder_detail_set.all()
    goodsdetail_list = []
    for i in goodsdetails:
        obj = {}
        obj['goodid'] = i.goodid
        obj['goodnum'] = i.goodnum
        obj['goodname'] = i.goodname
        obj['goodprice'] = i.goodprice
        goodsdetail_list.append(obj)
    data['goodsdetail'] = goodsdetail_list
    return JsonResponse({'status': 1, 'data': data})


def issended(request):
    orderid = request.GET.get('id')
    order = Xianchangorder.objects.get(id=orderid)
    if order.isget == 1:
        return JsonResponse({'status': 1})
    else:
        order.isget = 1
        order.save()
        return JsonResponse({'status': 1})






