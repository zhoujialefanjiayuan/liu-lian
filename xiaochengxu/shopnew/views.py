import datetime
import json

from django.db.models import Q
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.cache import cache_page

from news.views import to_dict
from shopnew.forpay import *
from shopnew.models import *
from shopping.pay import randnum

@cache_page(180)
def zhoubian_goods(request):
    zhoubians = Zhoubian.objects.exclude(isdelete=1).order_by('-id')
    outlist = []
    nameset = set()
    for i in zhoubians:
        obj = {}
        if i.name not in nameset:
            obj['name'] = i.name
            obj['price'] = i.price
            obj['id'] = i.id
            obj['main_img'] = i.main_img
            obj['description'] = i.describtion
            couponlist = []
            if i.canuse_coupon != '':
                inobj = {}
                thecoupon = Coupon.objects.get(id=i.canuse_coupon)
                inobj['require'] = thecoupon.require
                inobj['reduce'] = thecoupon.reduce
                couponlist.append(inobj)
            obj['couponlist'] =couponlist
            outlist.append(obj)
            nameset.add(i.name)
    topimg = Topimg.objects.get(type='zhoubian').img
    return JsonResponse({'status':1,'data':outlist,'topimg':topimg})

def thezhoubian(request):
    goodname = request.POST.get('goodname')
    allzhoubian = Zhoubian.objects.filter(name=goodname)
    sumnumber = 0
    for i in allzhoubian:
        sumnumber += i.storenum
    zhoubian = Zhoubian.objects.filter(name=goodname)[0]
    zhoubiandata = {}
    zhoubiandata['id']= zhoubian.id
    zhoubiandata['name']= zhoubian.name
    zhoubiandata['price']= zhoubian.price
    zhoubiandata['postage']= zhoubian.postage
    zhoubiandata['storenum']= sumnumber
    #优惠券
    couponlist = []
    if zhoubian.canuse_coupon != '':
        inobj = {}
        thecoupon = Coupon.objects.get(id = zhoubian.canuse_coupon)
        inobj['require'] = thecoupon.require
        inobj['reduce'] = thecoupon.reduce
        couponlist.append(inobj)
    zhoubiandata['canuse_coupon']= couponlist
    zhoubiandata['litter_img']= zhoubian.img1
    zhoubiandata['detail']= [ i for i in [zhoubian.detail1,zhoubian.detail2,zhoubian.detail3,zhoubian.detail4,zhoubian.detail5] if i != '']
    zhoubiandata['swiper_img']= [i for i in [zhoubian.img1,zhoubian.img2,zhoubian.img3,zhoubian.img4,zhoubian.img5] if i != '']
    return JsonResponse({'status':1,'data':zhoubiandata})

def getcale(request):
    goodname = request.POST.get('goodname')
    zhoubians = Zhoubian.objects.filter(name=goodname)
    size_list = []
    color_list = []
    store_list = []
    id_dict = {}
    for i in zhoubians:
        if i.size !='' or i.color != '':
            if i.size !='':
                size_list.append(i.size)
            if i.color != '':
                color_list.append(i.color)
            store_list.append([i.color,i.size,i.storenum])
            id_dict[i.color+i.size] = i.id
    size_list = list(set(size_list))
    color_list = list(set(color_list))
    return JsonResponse({'status':1,'size_list':size_list,'color_list':color_list,'store_list':store_list,'id_dict':id_dict})


def getlocation_note(request):
    userid = request.POST.get('userid')
    locations = Locationnote.objects.filter(userid=userid,isdelete=0).order_by('-id')
    location__list = []
    for i in locations:
        obj = {}
        region = i.region.split(',')
        obj['consignee'] = i.consignee
        obj['mobile'] = i.mobile
        obj['address'] = ''.join(region) + i.detailaddress
        obj['isdefult'] = i.isdefult
        obj['region'] = region
        obj['userAddress'] = ''.join(region)
        obj['detailAddress'] = i.detailaddress
        obj['id'] = i.id
        location__list.append(obj)
    return JsonResponse({'status':1,'location__list':location__list})

def record_location(request):
    # consignee: this.username,
    # mobile: this.userPhone,
    # address: this.userAddress + this.detailAddress,
    # isdefult: this.isDefult,
    # region: this.region,
    # userAddress: this.userAddress,
    # detailAddress: this.detailAddress
    userid = request.POST.get('userid')
    consignee = request.POST.get('consignee')
    region = request.POST.get('region')
    detailAddress = request.POST.get('detailAddress')
    mobile = request.POST.get('mobile')
    isdefult = request.POST.get('isdefult')
    if isdefult == 'true':
        isdefult = True
        thedefault = Locationnote.objects.filter(userid=userid, isdefult=1)
        if thedefault.exists():
            for i in thedefault:
                i.isdefult = 0
                i.save()
    else:
        isdefult = False
    Locationnote.objects.get_or_create(userid = userid,consignee=consignee,region=region,detailaddress=detailAddress,mobile=mobile,isdefult =isdefult)
    return JsonResponse({'status':1})

def del_location(request):
    locationid = request.POST.get('id')
    location = Locationnote.objects.get(id = int(locationid))
    location.isdelete = 1
    location.save()
    return JsonResponse({'status': 1})

def change_location(request):
    userid = request.POST.get('userid')
    consignee = request.POST.get('consignee')
    region = request.POST.get('region')
    detailAddress = request.POST.get('detailAddress')
    mobile = request.POST.get('mobile')
    isdefult = request.POST.get('isdefult')
    locationid = request.POST.get('locationid')
    location = Locationnote.objects.get(id = locationid)
    location.consignee = consignee
    location.region = region
    location.detailaddress = detailAddress
    location.mobile = mobile
    if isdefult == 'true':
        location.isdefult = True
        thedefault = Locationnote.objects.filter(userid=userid,isdefult=1)
        if thedefault.exists():
            for i in thedefault:
                i.isdefult = 0
                i.save()
    else:
        location.isdefult = False
    location.save()
    return JsonResponse({'status': 1})

def getdefault_location(request):
    userid = request.POST.get('userid')
    locationid = int(request.POST.get('locationid'))
    print('locationid>>>>',locationid)
    if locationid == 0:
        locations = Locationnote.objects.filter(userid=userid,isdefult=1,isdelete=0)
        if locations.exists():
            i = locations[0]
        else:
            locations = Locationnote.objects.filter(userid=userid,isdelete=0).order_by('-id')
            if locations.exists():
                i = locations[0]
            else:
                return JsonResponse({'status': 0, 'default_location': None})
    else:
        i = Locationnote.objects.get(id = locationid)
    obj = {}
    region = i.region.split(',')
    obj['consignee'] = i.consignee
    obj['mobile'] = i.mobile
    obj['address'] = ''.join(region) + i.detailaddress
    obj['isdefult'] = i.isdefult
    obj['region'] = region
    obj['userAddress'] = ''.join(region)
    obj['detailAddress'] = i.detailaddress
    obj['locationid'] = i.id
    return JsonResponse({'status': 1, 'default_location': obj})

def makeorder(request):
    location_id = request.POST.get('location_id')
    order_true_pay = request.POST.get('order_true_pay')
    note_cont = request.POST.get('note_cont')
    userid = request.POST.get('userid')
    postage = request.POST.get('postage')
    reduceprice = request.POST.get('reduceprice')
    #商品以对象的形式传入，
                # canuseCcoupon:[{…}]
                # goodId:2
                # goodImg:"http://xcx.szbeacon.com/000001.png"
                # goodName:"周笔畅LUNAR TOUR-中筒袜"
                # goodNum:1
                # goodPrice:"80.00"
                # goodType:"红36"
                # postage:10
                # storenum:10
    goodcar = request.POST.get('goodcar')
    goodcar = json.loads(goodcar)
    car_list = []
    for i in goodcar:
        obj={}
        obj['goodid'] = i['goodId']
        obj['goodnum'] = i['goodNum']
        obj['goodname'] = i['goodName']
        obj['goodprice'] = float(i['goodPrice'])
        obj['goodimg'] =i['goodImg']
        obj['goodtype'] =i['goodType']
        obj['idforcar'] =i.get('idforcar')
        car_list.append(obj)
    # 遍历购物车查询商品是否有库存或者失效
    returncode = {}
    print('car_list----',car_list)
    for i in car_list:
        num = int(i['goodnum'])
        goodid = int(i['goodid'])
        goodname = i['goodname']
        goodtype = i['goodtype']
        try:
            thezhoubian = Zhoubian.objects.get(id=goodid)
            if thezhoubian.storenum - num < 0:
                returncode[goodname + '-' +goodtype] = "仅剩"+ str(thezhoubian.storenum) + '件'
        except Exception as e:
            print('erro>>>',e)
            returncode[goodname + '-' +goodtype] = '商品失效'
    if len(returncode) > 0:
        returnerror =''
        for k in returncode:
            returnerror += k + returncode[k] + ';'
        return JsonResponse({'status': 0, 'code':returnerror})
    #清空购物车

    if car_list[0]['idforcar'] != None:
        for i in  car_list:
            idforcar = i['idforcar']
            goodincar = Car.objects.get(id=idforcar)
            goodincar.isdelete = 1
            goodincar.save()
    # 获取客户端ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip(若经过负载均衡，和代理有此项)
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    # 删除优惠券
    order = Zhoubianorders()
    now = datetime.datetime.now()
    order_num = randnum()
    order.order_num = order_num
    order.order_start_time = str(now)[:-7]
    order.order_true_pay = order_true_pay
    order.location_id = location_id
    order.note_cont = note_cont
    order.userid = userid
    order.postage_fee = postage
    order.coupon_reduce = reduceprice
    order.save()
    #存储订单详情
    goodstr = ''
    for i in car_list:
        detail = Zhoubianorder_detail()
        detail.goodid = i['goodid']
        detail.goodnum = i['goodnum']
        detail.goodname = i['goodname']
        detail.goodprice = i['goodprice']
        detail.goodimg = i['goodimg']
        detail.orderForeignKey = order
        detail.save()
        goodstr += i['goodname'] +'-'+i['goodtype']+ 'X' + str(i['goodnum'] )+', '
    #向微信下单
    forpay_data= pay_zhoubianorder(order_num, ip, order_true_pay, userid)
    thelocation = Locationnote.objects.get(id =location_id)
    order_data = {}
    order_data['order_num'] = order_num
    order_data['getman'] =thelocation.consignee
    order_data['order_phone'] = thelocation.mobile
    location_list = thelocation.region.split(',')
    order_data['d_province'] = location_list[0]
    order_data['d_city'] = location_list[1]
    order_data['d_county'] =location_list[2]
    order_data['d_address'] =thelocation.detailaddress
    order_data['goodname'] = goodstr +'留言' + note_cont
    order_data['goodcar'] = car_list
    return JsonResponse({'status':1,'forpay_data':forpay_data,'order_data':order_data})

#查询支付状态
def query_pay_state(request):
    order = request.POST.get('order_data')
    order = json.loads(order)
    print('>>>>>>',order)
    data = query_pay(order)
    if data['data'] == 'SUCCESS':
        #修改库存数据
        car = order['goodcar']
        for i in car:
            num = int(i['goodnum'])
            thezhoubian = Zhoubian.objects.get(id=i['goodid'])
            newstorenum = thezhoubian.storenum - num
            if newstorenum <0:
                thezhoubian.storenum = 0
            else:
                thezhoubian.storenum = newstorenum
            thezhoubian.save()
    return JsonResponse(data)


#购物车模块
def addtocar(request):
    goodid = request.POST.get('goodid')
    num = request.POST.get('num')
    userid = request.POST.get('userid')
    thegoodforcar = Car.objects.filter(userid=userid, goodid=goodid)
    if thegoodforcar.exists():
        car = thegoodforcar[0]
        if car.isdelete == 1:
            print('''222''')
            car.num = int(num)
            car.isdelete = 0
            car.save()
        else:
            car.num += int(num)
            car.save()
    else:
        car = Car()
        car.goodid = int(goodid)
        car.num = int(num)
        car.userid = userid
        car.save()
    return JsonResponse({'status': 1})

def showcar(request):
    userid = request.POST.get('userid')
    thedetails = Car.objects.filter(userid =userid,isdelete=0)
    zhoubian_list = []
    for i in thedetails:
        obj = {}
        goodid = i.goodid
        try:
            thegood = Zhoubian.objects.get(id = goodid)
        except:
            continue
        if thegood.storenum == 0:
            continue
        obj['name'] = thegood.name
        obj['price'] = thegood.price
        obj['postage'] = thegood.postage
        obj['img'] = thegood.img1
        obj['color'] = thegood.color
        obj['size'] = thegood.size
        obj['storenum'] = thegood.storenum
        obj['idforcar'] = i.id
        obj['goodid'] = goodid
        obj['goodnum'] = i.num
        couponlist = []
        if thegood.canuse_coupon != '':
            inobj = {}
            thecoupon = Coupon.objects.get(id=thegood.canuse_coupon)
            inobj['require'] = thecoupon.require
            inobj['reduce'] = thecoupon.reduce
            couponlist.append(inobj)
        obj['canuse_coupon'] = couponlist
        zhoubian_list.append(obj)
    return JsonResponse({'status': 1,'zhoubian_list':zhoubian_list})

def deltocar(request):
    idforcar = int(request.POST.get('idforcar'))
    thecar = Car.objects.get(id = idforcar)
    thecar.isdelete = 1
    thecar.save()
    return JsonResponse({'status': 1})

def getnumforcar(request):
    userid = request.POST.get('userid')
    if userid == '':
        return JsonResponse({'status': 1, 'num': 0})
    thedetails = Car.objects.filter(userid =userid,isdelete=0)
    num = 0
    for i in thedetails:
        goodid = i.goodid
        try:
            thegood = Zhoubian.objects.get(id=goodid)
        except:
            continue
        if thegood.storenum == 0:
            continue
        num += 1
    return JsonResponse({'status': 1,'num':num})


#获取我的周边订单
def myorder(request):
    userid = request.POST.get('userid')
    type = request.POST.get('type') #type传参，all  0-待支付，1-待收货，2-已收货交易完成售后，3-交易关闭
    order_list = []
    if type == 'all':
        orders = Zhoubianorders.objects.filter(userid=userid,isdelete =0).order_by('-id')
    else:
        orders = Zhoubianorders.objects.filter(Q(userid=userid) & Q(type=type)& Q(isdelete =0)).order_by('-id')
    if orders.exists():
        for i in orders:
            oneorder = {}
            goodcar_detail = i.zhoubianorder_detail_set.all()
            goods_detail_list = []
            payNum = 0
            print("商品id",[i.goodid for i in goodcar_detail])
            for j in goodcar_detail:
                innerobj = {}
                innerobj['goodid'] = j.goodid
                thegood = Zhoubian.objects.get(id = j.goodid)
                innerobj['goodimg'] = j.goodimg
                innerobj['goodname'] = j.goodname
                innerobj['goodnum'] = j.goodnum
                payNum += j.goodnum
                innerobj['goodprice'] = j.goodprice
                innerobj['goodtype'] = thegood.color + thegood.size
                goods_detail_list.append(innerobj)
            oneorder['goodcar'] = goods_detail_list
            oneorder['payNum'] = payNum
            oneorder['payMoney'] = i.order_true_pay
            oneorder['id'] = i.id
            oneorder['order_num'] = i.order_num
            oneorder['creat_time'] = i.order_start_time
            if i.type == 0:
                starttime = datetime.datetime.strptime(i.order_start_time, '%Y-%m-%d %H:%M:%S')
                print('time.time() - starttime.timestamp()',time.time() - starttime.timestamp())
                if time.time() - starttime.timestamp() > 1800:
                    i.type = 3
                    i.save()
                    oneorder['expiry_time'] = ''
                    oneorder['orderstatu'] = 3
                else:
                    oneorder['expiry_time'] = str( starttime+ datetime.timedelta(minutes=30))
                    oneorder['orderstatu'] = 0
            elif i.type == 1:
                if i.receivetime != "":
                    if time.time() - datetime.datetime.strptime(i.receivetime, '%Y-%m-%d %H:%M:%S').timestamp() > 604800:
                        i.type = 2
                        i.save()
                        oneorder['orderstatu'] = 2
                    else:
                        oneorder['orderstatu'] = 1
                else:
                    oneorder['orderstatu'] = 1
                oneorder['expiry_time'] = ''
            else:
                oneorder['expiry_time'] = ''
                oneorder['orderstatu'] = i.type
            order_list.append(oneorder)
    return JsonResponse({'status':1,'order_list':order_list})


def cancelorder(request):
    id = request.POST.get('id')
    theorder = Zhoubianorders.objects.get(id=id)
    theorder.type = 3
    theorder.save()
    return JsonResponse({'status':1})

def deleteorder(request):
    id = request.POST.get('id')
    theorder = Zhoubianorders.objects.get(id=id)
    theorder.isdelete =1
    theorder.save()
    return JsonResponse({'status': 1})

def makesure_get(request):
    id = request.POST.get('id')
    theorder = Zhoubianorders.objects.get(id=id)
    theorder.type = 2
    logistic = theorder.logistics
    if logistic is '':
        logistic = json.dumps([{'accept_time':'','accept_address':'','remark':'已确认收货，'}])
        theorder.logistics = logistic
    theorder.save()
    return JsonResponse({'status': 1})

def showtheorder(request):
    id = request.POST.get('id')
    print("id>>>",id)
    theorder = Zhoubianorders.objects.get(id = id)
    type = theorder.type
    oneorder = {}
    goodcar_detail = theorder.zhoubianorder_detail_set.all()
    goods_detail_list = []
    payNum = 0
    for j in goodcar_detail:
        innerobj = {}
        innerobj['goodid'] = j.goodid
        thegood = Zhoubian.objects.get(id=j.goodid)
        innerobj['goodimg'] = j.goodimg
        innerobj['goodname'] = j.goodname
        innerobj['goodnum'] = j.goodnum
        payNum += j.goodnum
        innerobj['goodprice'] = j.goodprice
        innerobj['goodtype'] = thegood.color + thegood.size
        goods_detail_list.append(innerobj)
    oneorder['goodcar'] = goods_detail_list
    oneorder['orderstatu'] = type
    oneorder['payNum'] = payNum
    oneorder['payMoney'] = theorder.order_true_pay
    oneorder['id'] = theorder.id
    oneorder['order_num'] = theorder.order_num
    oneorder['creat_time'] = theorder.order_start_time
    oneorder['pay_time'] = theorder.pay_time
    oneorder['leavewords'] = theorder.note_cont
    location_id = theorder.location_id
    location = Locationnote.objects.get(id = location_id)
    oneorder['location'] = to_dict(location)
    oneorder['postage'] = theorder.postage_fee
    oneorder['reduce'] = theorder.coupon_reduce
    if type == 0:
        starttime = datetime.datetime.strptime(theorder.order_start_time, '%Y-%m-%d %H:%M:%S')
        oneorder['logistics'] = ''
        if time.time() - starttime.timestamp() > 1800:
            theorder.type = 3
            theorder.save()
            oneorder['expiry_time'] = ''
        else:
            oneorder['expiry_time'] = str(starttime + datetime.timedelta(minutes=30))
    elif type == 1:
        oneorder['expiry_time'] = ''
        if theorder.logistics != '':
            logistics = json.loads(theorder.logistics)
            route_list = logistics
        # 物流查询,
        else:
            xml = query_xml(theorder.waybill_id)
            route_list = queryorder(xml)[1:]
            print(route_list)
        oneorder['logistics'] = [{'accept_time':'','accept_address':'','remark':'待顺丰网点揽件'}] if len(route_list) == 0 else route_list
        if oneorder['logistics'][-1]['accept_time'] != '':
            opcode = []
            for theopcode in route_list:
                opcode.append(theopcode['opcode'])
            if '80' in opcode:
                receivetime = route_list[-1]['accept_time']
                now = time.time()
                receive = datetime.datetime.strptime(receivetime, '%Y-%m-%d %H:%M:%S').timestamp()
                #存储物流信息
                theorder.logistics = json.dumps(route_list)
                theorder.receivetime = receivetime
                if now - receive > 604800:
                    theorder.type = 2
                theorder.save()
    elif type == 2:
        oneorder['expiry_time'] = ''
        logistics = json.loads(theorder.logistics)
        oneorder['logistics']  = logistics
    else:
        oneorder['expiry_time'] = ''
        oneorder['logistics'] = ''
    return JsonResponse({'status':1,'orderdata':oneorder})


#再次重新支付
def repay(request):
    old_order_num = request.POST.get('ordernum')
    car_list = request.POST.get('car_list')
    car_list = json.loads(car_list)
    goodstr = ''
    for i in car_list:
        goodstr += i['goodname'] + 'X' + str(i['goodnum']) + ', '
    # order = ZhouBianorders.objects.get(order_num=order_num)
    # now = time.time()
    # distance = now - int(order.timestamp)
    # if distance > (60*60*1.9):
    order = Zhoubianorders.objects.get(order_num=old_order_num)
    # 关闭订单
    data = close_pay(old_order_num)
    print('data',data)
    if data['result_code'] == 'FAIL':
        return JsonResponse({'status': 0, 'wx_data': '关闭订单失败'})
    # 重新发起支付，获取客户端ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip(若经过负载均衡，和代理有此项)
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    new_order_num = randnum()
    forpay_data = pay_zhoubianorder(new_order_num, ip, str(order.order_true_pay), order.userid)
    thelocation = Locationnote.objects.get(id=order.location_id)
    order_data = {}
    order_data['order_num'] = old_order_num
    order_data['new_order_num'] = new_order_num
    order_data['getman'] = thelocation.consignee
    order_data['order_phone'] = thelocation.mobile
    location_list = thelocation.region.split(',')
    order_data['d_province'] = location_list[0]
    order_data['d_city'] = location_list[1]
    order_data['d_county'] = location_list[2]
    order_data['d_address'] = thelocation.detailaddress
    order_data['goodname'] = goodstr + '留言:' + order.note_cont
    order_data['goodcar'] = car_list
    return JsonResponse({'status': 1, 'forpay_data': forpay_data, 'order_data': order_data})



