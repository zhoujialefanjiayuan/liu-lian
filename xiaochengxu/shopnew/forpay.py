import datetime
import os
import time
from django.http import JsonResponse

from shopnew.forfengqiao import *
from shopnew.models import Zhoubianorders

#微信支付统一下单接口
from shopnew.pay import *

url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
appid =	'wx16360426dc864b7d'
mch_id = '1537642871'
trade_type = 'JSAPI'
key = '1234567890QWERTYUIOPASDFGHJKLZXC'
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
    print('response')
    response = requests.post(url,data=xml_params)
    print(response)
    get_dict = trans_xml_to_dict(response.text)
    return get_dict

#查询支付状态
def query_pay(obj):
    if obj.get('new_order_num') != None:
        order_num = obj.get('new_order_num')
    else:
        order_num = obj.get('order_num')
    params = {
        'appid': appid,
        'mch_id': mch_id,
        'out_trade_no': order_num,
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
    #支付成功
    if state == 'SUCCESS':
        # 生成物流订单
        sendtime = str(datetime.datetime.now() + datetime.timedelta(days=1))[:10]
        obj['sendtime'] = sendtime
        xml = compose_addorderxml(obj)
        response = addorder(xml)
        try:
            mailno = response['mailno']
        except:
            #查询物流状态
            res = getstatu(obj['order_num'])
            mailno = res['mailno']
        #存储订单
        order = Zhoubianorders.objects.get(order_num=obj['order_num'])
        order.type = 1
        order.ispay = 1
        order.order_num = order_num
        order.pay_time = str(datetime.datetime.now())[:-7]
        order.waybill_id = mailno
        order.save()
        #存储订单文件
        ordertxt = """{
            "consignerAddress": "%s",
        	"consignerCity": "%s",
        	"consignerCounty": "%s",
        	"consignerName": "%s",
        	"consignerProvince": "%s",
        	"consignerTel": "%s",
        	"deliverAddress": "T-Park深港影视创意园708",
        	"deliverCity": "深圳市",
        	"deliverCompany": "榴莲音乐科技（深圳）有限公司",
        	"deliverCounty": "福田区",
        	"deliverMobile": "0755-26806888",
        	"deliverName": "张先生",
        	"deliverProvince": "广东省",
        	"deliverTel": "0755-26806888",
        	"encryptCustName": "true",
        	"encryptMobile": "true",
        	"expressType": "2",
        	"mailNo": "%s", 
        	"mainRemark": "%s",
        	"monthAccount": "7550069706",
        	"payMethod": "1",
        	"rlsInfoDtoList": [{
        		"twoDimensionCode": "MMM={'k1':'755WE','k2':'021WT','k3':'','k4':'T4','k5':'SF7551234567890','k6':''}",
        		"abFlag": "A",
        		"codingMapping": "F33",
        		"codingMappingOut": "1A",
        		"destRouteLabel": "755WE-571A3",
        		"proCode": "T6", 
        		"sourceTransferCode": "021WTF",
        		"waybillNo": "%s",
        		"xbFlag": "XB"
        	}],
        	"zipCode": "755"}
        """ % (obj['d_address'], obj['d_city'], obj['d_county'],obj['getman'], obj['d_province'],
               obj['order_phone'], mailno, obj['goodname'], mailno)
        savedirurl = r"/home/zhou/zhoubianorder/%s"%order.order_start_time[:10]
        savetxturl = r"/home/zhou/zhoubianorder/%s/%s.txt"%(order.order_start_time[:10],mailno)
        if os.path.exists(savedirurl) == False:
            os.makedirs(savedirurl)
        with open(savetxturl,'w') as fp:
            fp.write(ordertxt)
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

#向微信下单支付
def pay_zhoubianorder(order_num,ip,order_true_pay,order_user):
    #微信统一下单接口
    body = 'test'  # 类目
    out_trade_no = order_num  # 商户订单号
    total_fee = int(float(order_true_pay)*100) # 支付金额，单位分
    spbill_create_ip = ip  # 终端ip
    notify_url = 'https://www.jianshu.com/u/44cde87b5c30'  # 支付后的通知回调url
    data_params = get_params(body, out_trade_no, total_fee, spbill_create_ip,order_user[:-3],notify_url)
    xml_params = get_xml_params(data_params, key)
    response_dict = pay_wx(xml_params)
    print("........>>>>d",response_dict)
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
    return send_data




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


# # 退款
# def refundment(request):
#     order_num = request.GET.get('order_num')
#     order = ZhouBianorders.objects.get(order_num=order_num)
#     if order.type == 41:
#         order_true_pay = int(order.order_true_pay*100)
#         notify_url = 'http://101.132.47.14/shop/get_wxnotice_refund/'
#         url = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
#         params = {
#             'appid': appid,
#             'mch_id': mch_id,
#             'nonce_str': randnum(),
#             'out_trade_no': order_num,
#             'out_refund_no':order_num,
#             'total_fee': order_true_pay,
#             'refund_fee': order_true_pay,
#             'notify_url': notify_url,
#         }
#         xml_params = get_xml_params(params, key)
#         headers = {'Content-Type': 'application/xml'}
#         ssh_keys_path = '/home/zhou/project/xiaochengxu/cert'
#         weixinapiclient_cert = os.path.join(ssh_keys_path, "apiclient_cert.pem")
#         weixinapiclient_key = os.path.join(ssh_keys_path, "apiclient_key.pem")
#
#         res = requests.post(url, data=xml_params, headers=headers,
#                             cert=(weixinapiclient_cert, weixinapiclient_key), verify=True)
#         get_dict = trans_xml_to_dict(res.text)
#         if get_dict['result_code'] == 'SUCCESS':
#             #提交退款成功
#             refund = Refund()
#             refund.order_num = order_num
#             refund.refund_num = order.order_true_pay
#             refund.save()
#             time.sleep(3)
#             return HttpResponseRedirect('/admin/shopping/zhoubianorders/')
#     else:
#         return JsonResponse({'status': 1,'code':'FAIL'})
#
# #获取退款结果通知
# def get_wxnotice_refund(request):
#     data = request.body.decode()
#     data_dict = trans_xml_to_dict(data)
#     if data_dict['return_code'] == 'SUCCESS':
#         req_info = data_dict['req_info']
#         md5 = hashlib.md5()  # 使用MD5加密模式
#         md5.update(key.encode('utf-8'))  # 将参数字符串传入
#         tokey = md5.hexdigest().lower()
#         code = base64.b64decode(req_info)
#         cipher = AES.new(tokey, AES.MODE_ECB).decrypt(code).decode()
#         res_data = trans_xml_to_dict(cipher,'root')
#
#         order_true_pay = float(res_data['total_fee'])/100
#         order_num = res_data['out_trade_no']
#         refund = Refund.objects.get(order_num=order_num)
#         if refund.refund_status ==0:
#             refund.refund_status = 1
#             refund.save()
#             order = ZhouBianorders.objects.filter(order_num=order_num)[0]
#             order.type = 43
#             order.save()
#             return JsonResponse({'status': 1})
#         else:
#             return JsonResponse({'status': 1})
#



# #申请退货
# def return_goods(request):
#     order_num = request.POST.get('order_num')
#     order = ZhouBianorders.objects.filter(order_num=order_num)[0]
#     if order.type == 32:
#         order.type = 41
#         order.save()
#         return JsonResponse({'status': 1,'code':'succese'})
#     else:
#         return JsonResponse({'status': 0,'code':'该状态不支持退款'})

# #取消退款
# def cancel_return(request):
#     order_num = request.POST.get('order_num')
#     order = ZhouBianorders.objects.filter(order_num=order_num)[0]
#     order_start_time = order.order_start_time
#     if order.type == 41:
#         now = time.time()
#         start = datetime.datetime.strptime(order_start_time, '%Y-%m-%d %H:%M:%S').timestamp()
#         if now - start > 604800:
#             order.type = 31
#         else:
#             order.type = 32
#         order.save()
#         return JsonResponse({'status': 1})
#     else:
#         return JsonResponse({'status': 0,'code':'该状态不支持取消退款'})
#
# #拒绝退款
# def refuse_return(request):
#     order_num = request.GET.get('order_num')
#     print('order_num',order_num)
#     order = ZhouBianorders.objects.filter(order_num=order_num)[0]
#     if order.type == 41:
#         order.type = 42
#         order.save()
#         return HttpResponseRedirect('/admin/shopping/zhoubianorders/')
#     else:
#         return JsonResponse({'status': 0,'code':'该状态不支持拒绝退款'})





