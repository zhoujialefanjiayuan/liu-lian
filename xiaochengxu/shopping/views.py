import datetime
import json
import os
import time

import random
import requests
from Crypto.Cipher import AES
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.cache import cache_page

from activety.models import Usercoupon
from news.views import to_dict
from shopping.fengqiao import *
from shopping.models import *
from shopping.pay import *

#微信支付统一下单接口


url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
appid =	'wx16360426dc864b7d'
mch_id = '1537642871'
trade_type = 'JSAPI'
key = '123456789qwertyuiopasdfghjklzxcv'
clientCode = 'LLYLKJSZ'
checkWord = 'STGuVhBlDznxZbvyFFSxP5fdsyH8geFq'
"""
可变参数
body = 'test' #类目
out_trade_no = '20191210' #商户订单号
total_fee = 88 #支付金额，单位分
spbill_create_ip = '14.23.150.211'  #终端ip
notify_url = 'https://www.jianshu.com/p/40c7bd9388a6'  #通知回调url
"""
def get_params(body,out_trade_no,total_fee,spbill_create_ip,openid,notify_url):
    data_params = {
        'appid':appid,
        'mch_id':mch_id,
        'body':body,
        'out_trade_no':out_trade_no,
        'total_fee':total_fee,
        'spbill_create_ip':spbill_create_ip,
        'trade_type':trade_type,
        'notify_url':notify_url,
        'nonce_str':randnum(),
        'openid':openid
    }
    return data_params

#生成sign,并生成xml参数data_params(没有含有sign)
def get_xml_params(data_params,key):
    sign = get_sign(data_params, key)
    data_params['sign'] = sign
    xml_params = trans_dict_to_xml(data_params)
    return xml_params

#发起请求，调用微信支付接口
def pay_wx(xml_params):
    response = requests.post(url,data=xml_params)
    get_dict = trans_xml_to_dict(response.text)
    return get_dict

#查询支付状态
def query_pay(obj):
    params = {
        'appid': appid,
        'mch_id': mch_id,
        'out_trade_no': obj['order_num'],
        'nonce_str': randnum(),
    }
    sign = get_sign(params, key)
    params['sign'] = sign
    xml_params = trans_dict_to_xml(params)
    #查询订单
    url = 'https://api.mch.weixin.qq.com/pay/orderquery'
    res = requests.post(url,data=xml_params)
    get_dict = trans_xml_to_dict(res.text)
    state = get_dict['trade_state']
    if state == 'SUCCESS':
        # 生成物流订单
        xml = compose_addorderxml(obj)
        response = addorder(xml)
        try:
            mailno = response['mailno']
        except:
            #查询物流状态
            res = getstatu(obj['order_num'])
            mailno = response['mailno']
        #存储订单
        order = ZhouBianorders()
        order.order_location = obj['order_location']
        order.order_phone = obj['order_phone']
        order.getman = obj['getman']
        order.order_num = obj['order_num']
        order.order_user = obj['order_user']
        order.order_start_time = obj['order_start_time']
        order.order_true_pay =obj['order_true_pay']
        order.goodnum =obj['goodnum']
        order.type = 2
        order.couponid = 0 if obj['couponid'] == '' else obj['couponid']
        order.zhoubianid = obj['zhoubianid']
        order.goodname = obj['goodname']
        order.goodimg = obj['goodimg']
        order.goodprice = obj['goodprice']
        order.waybill_id = response['mailno']
        order.save()
        return {'status':1,'data':'SUCCESS'}
    else:
        return {'status':0,'data':state}

#关闭订单
def close_pay(order_num):
    params = {
        'appid': appid,
        'mch_id': mch_id,
        'out_trade_no': order_num,
        'nonce_str': randnum(),
    }
    sign = get_sign(params, key)
    params['sign'] = sign
    xml_params = trans_dict_to_xml(params)
    #关订单
    url = 'https://api.mch.weixin.qq.com/pay/closeorder'
    res = requests.post(url,data=xml_params)
    get_dict = trans_xml_to_dict(res.text)
    #关闭物流单
    xml = compose_delorderxml(order_num)
    fengqiaodelorder(xml)
    return get_dict

def closeorder(request):
    order_num = request.POST.get('order_num')
    get = close_pay(order_num)
    result_code = get['result_code']
    if result_code == 'SUCCESS':
        return JsonResponse({'status':1,'code':'SUCCESS'})
    else:
        return JsonResponse({'status': 0, 'code': 'FAIL'})


@cache_page(60*60,cache='longtime')
def goods_type(request):
    types = Good_types.objects.all()
    data =[]
    for type in types:
        obj = {}
        obj['type_id'] = type.id
        obj['type_name']=type.type_name
        obj['type_icon']=type.type_icon
        obj['color']='#6e6d6d'
        data.append(obj)
    return JsonResponse({'status':1,'data':data})

# def goods(request):
#     goods = Goods.objects.all()
#     types = Good_types.objects.all()
#     typecontent = []
#     for type in types:
#         obj = {}
#         obj['type_id'] = type.id
#         obj['type_name'] = type.type_name
#         obj['type_icon'] = type.type_icon
#         obj['color'] = '#6e6d6d'
#         typecontent.append(obj)
#     data = {}
#     for good in goods:
#         type = good.type
#         if type in data:
#             goodlist = data[type]
#             obj_in = {}
#             obj_in['good_id'] = good.id
#             obj_in['good_name'] = good.goods_name
#             obj_in['goods_price'] = float(good.goods_price)
#             obj_in['store_num'] = good.store_num
#             obj_in['description'] = good.description
#             obj_in['picture'] = good.picture
#             obj_in['num'] = 0
#             obj_in['type'] = type
#             goodlist.append(obj_in)
#         else:
#             goodlist = []
#             obj_in = {}
#             obj_in['good_id'] = good.id
#             obj_in['good_name'] = good.goods_name
#             obj_in['goods_price'] = float(good.goods_price)
#             obj_in['store_num'] = good.store_num
#             obj_in['description'] = good.description
#             obj_in['picture'] = good.picture
#             obj_in['num'] = 0
#             obj_in['type'] = type
#             goodlist.append(obj_in)
#             data[type] = goodlist
#     datalist = [{'type':k,'data':v} for k,v in data.items()]
#     return JsonResponse({'status': 1, 'data': datalist,'typecontent':typecontent})



#周边商品
@cache_page(60*60,cache='longtime')
def showzhoubian(request):
    zhoubians = Zhoubian.objects.all()
    data = []
    for zhoubian in zhoubians:
        obj = {}
        obj['img'] = zhoubian.img
        obj['name'] = zhoubian.name
        obj['price'] = zhoubian.price
        obj['log'] = zhoubian.log
        obj['id'] = zhoubian.id
        data.append(obj)
    return JsonResponse({'status':1,'data':data})

#周边详情
@cache_page(60*60,cache='longtime')
def thezhoubian(request):
    id = int(request.GET.get('zhoubianid'))
    zhoubian = Zhoubian.objects.get(id = id)
    obj = {}
    obj['img'] = zhoubian.img
    obj['name'] = zhoubian.name
    obj['price'] = zhoubian.price
    obj['log'] = zhoubian.log
    obj['id'] = zhoubian.id
    ll = [zhoubian.detail1,zhoubian.detail2,zhoubian.detail3,zhoubian.detail4]
    obj['detail'] =[i for i in ll if i != '']
    return JsonResponse({'status': 1, 'data': obj})

#15分钟后若任然是未支付，则删除订单
def delorder(order_num):
    time.sleep(910)
    order = ZhouBianorders.objects.filter(order_num=order_num)
    if order.exists() and order[0].type == 1:
        order.delete()


#提交周边订单
def post_zhoubianorder(request):
    order_user = request.POST.get('userid')
    order_location = request.POST.get('location')
    order_phone = request.POST.get('phone')
    order_couponid = request.POST.get('couponid')
    order_true_pay = request.POST.get('true_pay')
    getman = request.POST.get('getman')
    goodnum = request.POST.get('goodnum')
    zhoubianid = request.POST.get('zhoubianid')

    #获取客户端ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip(若经过负载均衡，和代理有此项)
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip

    zhoubian = Zhoubian.objects.get(id=int(zhoubianid))
    order_num = randnum()
    #删除优惠券
    if order_couponid != '':
        usercou = Usercoupon.objects.filter(Q(userid=order_user)&Q(coupon_id =int(order_couponid)))
        if usercou.exists():
            usercou[0].delete()
    #微信统一下单接口
    body = 'test'  # 类目
    out_trade_no = order_num  # 商户订单号
    total_fee = int(float(order_true_pay)*100) # 支付金额，单位分
    spbill_create_ip = ip  # 终端ip
    notify_url = 'https://www.jianshu.com/u/44cde87b5c30'  # 支付后的通知回调url
    data_params = get_params(body, out_trade_no, total_fee, spbill_create_ip,order_user[:-3],notify_url)
    xml_params = get_xml_params(data_params, key)
    response_dict = pay_wx(xml_params)
    # {'return_code': 'SUCCESS', 'trade_type': 'JSAPI', 'prepay_id': 'wx18102325542417b42cdbe9ef1001807600',
    #  'mch_id': '1537642871', 'sign': '36DEB26F5187D2DB8ABE839373EC09F1', 'return_msg': 'OK',
    #  'appid': 'wx16360426dc864b7d', 'result_code': 'SUCCESS', 'nonce_str': 'vVqn4SuQts0v18iE'}
    timestamp = str(int(time.time()))
    send_data = {}
    send_data['timeStamp']= timestamp
    send_data['appId']= response_dict['appid']
    send_data['signType']= 'MD5'
    send_data['nonceStr']= response_dict['nonce_str'].upper()
    send_data['package']= 'prepay_id='+ response_dict['prepay_id']
    send_sign = get_sign(send_data, key)
    send_data['sign'] = send_sign
    send_data['order_num'] = order_num

    #订单数据
    obj = {}
    obj['order_location'] = order_location
    obj['order_phone'] = order_phone
    obj['getman'] = getman
    obj['order_num'] = order_num
    obj['order_user'] = order_user
    now = datetime.datetime.now()
    end = now + datetime.timedelta(minutes=10)
    obj['order_start_time'] = str(now)[:-7]
    obj['order_end_time'] = str(end)[:-7]
    obj['order_true_pay'] = order_true_pay
    obj['goodnum'] = goodnum
    obj['type'] = 1
    obj['couponid'] = order_couponid
    obj['zhoubianid'] = zhoubian.id
    obj['goodname'] = zhoubian.name
    obj['goodimg'] = zhoubian.img
    obj['goodprice'] = zhoubian.price

    return JsonResponse({'status': 1,'wx_data':send_data,'order_data':obj})

#获取支付结果通知
def get_wxnotice_pay(request):
    # data = request.body.decode()
    # data_dict = trans_xml_to_dict(data)
    # if data_dict['return_code'] == 'SUCCESS':
    #     order_num = data_dict['out_trade_no']
    #     order_true_pay = data_dict['total_fee']
    #     order = ZhouBianorders.objects.filter(Q(order_num=order_num)&Q(order_true_pay=order_true_pay))[0]
    #     order.type = 2
    #     order.save()
    return JsonResponse({'status': 1})


#待支付再次调用支付
def ready_pay(request):
    order = request.POST.get('order_data')

    # order = ZhouBianorders.objects.get(order_num=order_num)
    # now = time.time()
    # distance = now - int(order.timestamp)
    # if distance > (60*60*1.9):
    # 关闭订单
    old_order_num = order['order_num']
    data = close_pay(old_order_num)
    if data['result_code'] == 'FAIL':
          return JsonResponse({'status':0,'wx_data':'关闭订单失败'})
    # 重新发起支付，获取客户端ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip(若经过负载均衡，和代理有此项)
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    # new_order_num = randnum()
    order_true_pay = order['order_true_pay']
    order_user = order['order_user']
    # 微信统一下单接口
    body = 'test'  # 类目
    out_trade_no = old_order_num  # 商户订单号
    total_fee = int(float(order_true_pay) * 100)  # 支付金额，单位分
    spbill_create_ip = ip  # 终端ip
    notify_url = 'https://www.jianshu.com/u/44cde87b5c30'  # 支付后的通知回调url
    data_params = get_params(body, out_trade_no, total_fee, spbill_create_ip,order_user[:-3],notify_url)
    xml_params = get_xml_params(data_params, key)
    response_dict = pay_wx(xml_params)
    # {'return_code': 'SUCCESS', 'trade_type': 'JSAPI', 'prepay_id': 'wx18102325542417b42cdbe9ef1001807600',
    #  'mch_id': '1537642871', 'sign': '36DEB26F5187D2DB8ABE839373EC09F1', 'return_msg': 'OK',
    #  'appid': 'wx16360426dc864b7d', 'result_code': 'SUCCESS', 'nonce_str': 'vVqn4SuQts0v18iE'}
    timestamp = str(int(time.time()))
    send_data = {}
    send_data['timeStamp'] = timestamp
    send_data['appId'] = response_dict['appid']
    send_data['signType'] = 'MD5'
    send_data['nonceStr'] = response_dict['nonce_str'].upper()
    send_data['package'] = 'prepay_id=' + response_dict['prepay_id']
    send_sign = get_sign(send_data, key)
    send_data['sign'] = send_sign
    send_data['order_num'] = old_order_num

    # 重新存储订单
    # order.order_num = new_order_num
    # order.timestamp = timestamp
    # order.save()
    # delorder(order_num)

    return JsonResponse({'status': 1, 'wx_data': send_data, 'order_data': order})


# 退款
def refundment(request):
    order_num = request.GET.get('order_num')
    order = ZhouBianorders.objects.get(order_num=order_num)
    if order.type == 41:
        order_true_pay = int(order.order_true_pay*100)
        notify_url = 'http://101.132.47.14:8000/shop/get_wxnotice_refund/'
        url = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
        params = {
            'appid': appid,
            'mch_id': mch_id,
            'nonce_str': randnum(),
            'out_trade_no': order_num,
            'out_refund_no':order_num,
            'total_fee': order_true_pay,
            'refund_fee': order_true_pay,
            'notify_url': notify_url,
        }
        xml_params = get_xml_params(params, key)
        headers = {'Content-Type': 'application/xml'}
        ssh_keys_path = '/home/zhou/project/xiaochengxu/cert'
        weixinapiclient_cert = os.path.join(ssh_keys_path, "apiclient_cert.pem")
        weixinapiclient_key = os.path.join(ssh_keys_path, "apiclient_key.pem")

        res = requests.post(url, data=xml_params, headers=headers,
                            cert=(weixinapiclient_cert, weixinapiclient_key), verify=True)
        get_dict = trans_xml_to_dict(res.text)
        if get_dict['result_code'] == 'SUCCESS':
            #提交退款成功
            refund = Refund()
            refund.order_num = order_num
            refund.refund_num = order.order_true_pay
            refund.save()
            time.sleep(3)
            return HttpResponseRedirect('/admin/shopping/zhoubianorders/')
    else:
        return JsonResponse({'status': 1,'code':'FAIL'})

#获取退款结果通知
def get_wxnotice_refund(request):
    data = request.body.decode()
    data_dict = trans_xml_to_dict(data)
    if data_dict['return_code'] == 'SUCCESS':
        req_info = data_dict['req_info']
        md5 = hashlib.md5()  # 使用MD5加密模式
        md5.update(key.encode('utf-8'))  # 将参数字符串传入
        tokey = md5.hexdigest().lower()
        code = base64.b64decode(req_info)
        cipher = AES.new(tokey, AES.MODE_ECB).decrypt(code).decode()
        res_data = trans_xml_to_dict(cipher,'root')

        order_true_pay = float(res_data['total_fee'])/100
        order_num = res_data['out_trade_no']
        refund = Refund.objects.get(order_num=order_num)
        if refund.refund_status ==0:
            refund.refund_status = 1
            refund.save()
            order = ZhouBianorders.objects.filter(order_num=order_num)[0]
            order.type = 43
            order.save()
            return JsonResponse({'status': 1})
        else:
            return JsonResponse({'status': 1})



#查询支付状态
def query_pay_state(request):
    order = request.POST.get('order_data')
    obj = json.loads(order)
    data = query_pay(obj)
    return JsonResponse(data)

#获取我的订单
def myorder(request):
    userid = request.POST.get('userid')
    type = int(request.POST.get('type'))
    if type == 2:
        orders = ZhouBianorders.objects.filter(Q(order_user=userid) & Q(type=2)).order_by('-id')
    elif type == 3:
        orders = ZhouBianorders.objects.filter( (Q(order_user=userid)&Q(type=31))|(Q(order_user=userid)&Q(type=32)) ).order_by('-id')
    else:
        orders = ZhouBianorders.objects.filter( (Q(order_user=userid)&Q(type=41))|(Q(order_user=userid)&Q(type=42))|(Q(order_user=userid)&Q(type=43)) ).order_by('-id')
    order_data = []
    if orders.exists():
        for order in orders:
            obj = {}
            if type == 2:
                #物流查询
                xml = query_xml(order.order_num)
                route_list = queryorder(xml)
                if 'remark' in route_list[-1]:
                    obj['trans']= route_list[-1]['remark']
                    opcode = route_list[-1]['opcode']
                    if opcode == '80':
                        receivetime = route_list[-1]['accept_time']
                        now = time.time()
                        receive = datetime.datetime.strptime(receivetime, '%Y-%m-%d %H:%M:%S').timestamp()
                        if now - receive > 604800:
                            order.type = 31
                            order.receivetime = receivetime
                            order.save()
                        else:
                            order.type = 32
                            order.receivetime = receivetime
                            order.save()
                else:
                    obj['trans'] = '待揽件'
            elif type == 3:
                #判断是否过七天
                if order.type == 32:
                    now = time.time()
                    receive = datetime.datetime.strptime(order.receivetime, '%Y-%m-%d %H:%M:%S').timestamp()
                    if now - receive > 604800:
                        order.type = 31
                        order.save()
            obj['order_num'] = order.order_num
            obj['order_id'] = order.id
            obj['order_start_time'] = order.order_start_time
            obj['order_true_pay'] = order.order_true_pay
            obj['goodnum'] = order.goodnum
            obj['type'] = order.type
            obj['goodname'] = order.goodname
            obj['goodimg'] = order.goodimg
            obj['goodprice'] = order.goodprice
            order_data.append(obj)
    return JsonResponse({'status': 1,'order_list':order_data,'type':type})

#申请退货
def return_goods(request):
    order_num = request.POST.get('order_num')
    order = ZhouBianorders.objects.filter(order_num=order_num)[0]
    if order.type == 32:
        order.type = 41
        order.save()
        return JsonResponse({'status': 1,'code':'succese'})
    else:
        return JsonResponse({'status': 0,'code':'该状态不支持退款'})

#取消退款
def cancel_return(request):
    order_num = request.POST.get('order_num')
    order = ZhouBianorders.objects.filter(order_num=order_num)[0]
    order_start_time = order.order_start_time
    if order.type == 41:
        now = time.time()
        start = datetime.datetime.strptime(order_start_time, '%Y-%m-%d %H:%M:%S').timestamp()
        if now - start > 604800:
            order.type = 31
        else:
            order.type = 32
        order.save()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0,'code':'该状态不支持取消退款'})

#拒绝退款
def refuse_return(request):
    order_num = request.GET.get('order_num')
    print('order_num',order_num)
    order = ZhouBianorders.objects.filter(order_num=order_num)[0]
    if order.type == 41:
        order.type = 42
        order.save()
        return HttpResponseRedirect('/admin/shopping/zhoubianorders/')
    else:
        return JsonResponse({'status': 0,'code':'该状态不支持拒绝退款'})

#现场服务
@cache_page(60*60,cache='longtime')
def newgoods(request):
    goods = Goods.objects.all()
    types = Good_types.objects.all()
    typecontent = []
    for type in types:
        obj = {}
        obj['type_id'] = type.id
        obj['type_name'] = type.type_name
        obj['type_icon'] = type.type_icon
        obj['color'] = '#6e6d6d'
        typecontent.append(obj)
    data = {}
    for good in goods:
        type = good.type
        if type in data:
            gooddict = data[type]
            obj_in = {}
            id = good.id
            obj_in['good_id'] = id
            obj_in['good_name'] = good.goods_name
            obj_in['goods_price'] = float(good.goods_price)
            obj_in['store_num'] = good.store_num
            obj_in['description'] = good.description
            obj_in['picture'] = good.picture
            obj_in['num'] = 0
            obj_in['type'] = type
            gooddict[id] = obj_in
        else:
            gooddict = {}
            obj_in = {}
            id = good.id
            obj_in['good_id'] = id
            obj_in['good_name'] = good.goods_name
            obj_in['goods_price'] = float(good.goods_price)
            obj_in['store_num'] = good.store_num
            obj_in['description'] = good.description
            obj_in['picture'] = good.picture
            obj_in['num'] = 0
            obj_in['type'] = type
            gooddict[id] = obj_in
            data[type] = gooddict
    return JsonResponse({'status': 1, 'data': data,'typecontent':typecontent})



def post_xianchangorder(request):
    order_userid = request.POST.get('userid')
    location_site = request.POST.get('location_site')
    location_seat = request.POST.get('location_seat')
    phone = request.POST.get('phone')
    couponid = request.POST.get('couponid')
    order_true_pay = request.POST.get('true_pay')
    order_getman = request.POST.get('getman')
    goodbag = request.POST.get('goodbag')
    goodbag = json.loads(goodbag)
    # 获取客户端ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip(若经过负载均衡，和代理有此项)
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    order = Xianchangorder()
    now = datetime.datetime.now()
    ordernum = randnum()
    order.order_num = ordernum
    order.order_start_time = str(now)[:-7]
    order.order_userid = order_userid
    order.order_getman = order_getman
    order.location_site = location_site
    order.location_seat = location_seat
    order.phone = phone
    order.couponid = 0 if couponid == '' else int(couponid)
    order.order_true_pay = order_true_pay
    order.save()
    for goodid in goodbag:
        detail = Xianchangorder_detail()
        detail.goodid = goodbag[goodid]['good_id']
        detail.goodnum = goodbag[goodid]['num']
        detail.goodname = goodbag[goodid]['good_name']
        detail.goodprice = goodbag[goodid]['goods_price']
        detail.ordernum = ordernum
        detail.orderForeignKey = order
        detail.save()

    #删除优惠券
    if couponid != '':
        usercou = Usercoupon.objects.filter(Q(userid=order_userid)&Q(coupon_id =int(couponid)))
        if usercou.exists():
            usercou[0].delete()
    #微信统一下单接口
    body = 'test'  # 类目
    out_trade_no = ordernum  # 商户订单号
    total_fee = int(float(order_true_pay)*100) # 支付金额，单位分
    spbill_create_ip = ip  # 终端ip
    notify_url = 'https://www.jianshu.com/u/44cde87b5c30'  # 支付后的通知回调url
    data_params = get_params(body, out_trade_no, total_fee, spbill_create_ip,order_userid[:-3],notify_url)
    xml_params = get_xml_params(data_params, key)
    response_dict = pay_wx(xml_params)
    timestamp = str(int(time.time()))
    send_data = {}
    send_data['timeStamp']= timestamp
    send_data['appId']= response_dict['appid']
    send_data['signType']= 'MD5'
    send_data['nonceStr']= response_dict['nonce_str'].upper()
    send_data['package']= 'prepay_id='+ response_dict['prepay_id']
    send_sign = get_sign(send_data, key)
    send_data['sign'] = send_sign
    send_data['order_num'] = ordernum

    return JsonResponse({'status': 1, 'wx_data': send_data})

def qureypay_forxianchang(request):
    order_num = request.POST.get('order_num')
    params = {
        'appid': appid,
        'mch_id': mch_id,
        'out_trade_no': order_num,
        'nonce_str': randnum(),
    }
    sign = get_sign(params, key)
    params['sign'] = sign
    xml_params = trans_dict_to_xml(params)
    # 查询订单
    url = 'https://api.mch.weixin.qq.com/pay/orderquery'
    res = requests.post(url, data=xml_params)
    get_dict = trans_xml_to_dict(res.text)
    if get_dict['result_code'] == 'SUCCESS':
        state = get_dict['trade_state']
        if state == 'SUCCESS':
            theorder = Xianchangorder.objects.get(order_num = order_num)
            theorder.ispay = 1
            theorder.save()
            return JsonResponse({'status': 1, 'code': 'SUCCESS'})
        else:
            return JsonResponse({'status': 0, 'code': 'FAIL'})
    else:
        return JsonResponse({'status': 0, 'code': 'FAIL'})


def showorder_forxianchang(request):
    userid = request.POST.get('userid')
    orders = Xianchangorder.objects.filter(order_userid=userid,ispay=1).order_by('-id')
    wait = []
    get = []
    if orders.exists:
        for order in orders:
            obj = to_dict(order)
            ordernum = obj['order_num']
            details = Xianchangorder_detail.objects.filter(ordernum=ordernum)
            detail_list = []
            for detail in details:
                inner = {}
                inner['goodname'] = detail.goodname
                inner['goodnum'] = detail.goodnum
                inner['goodprice'] = detail.goodprice
                detail_list.append(inner)
            obj['detail_list'] = detail_list
            sum = 0
            for the in detail_list:
                sum += the['goodnum'] * the['goodprice']
            obj['coupon'] =  sum - obj['order_true_pay']
            obj['sum'] =  sum
            if obj['isget'] == 0:
                wait.append(obj)
            else:
                get.append(obj)
    return JsonResponse({'waitorder':wait,'got':get})







