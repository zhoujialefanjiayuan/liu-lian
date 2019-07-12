import time
from math import floor, ceil

import random

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page

from activety.models import *
from paly.models import User
from news.views import to_dict
from django.http import JsonResponse


#所有的活动
@cache_page(60*5,cache='longtime')
def allactivety(request):
    activeties = Activety.objects.all().order_by('endtime')
    data_list = []
    for i in activeties:
        obj = {}
        obj['img']=i.img
        obj['id']=i.id
        obj['name']=i.name
        obj['support']=i.support
        obj['endtime']=str(i.endtime)[:19].replace('T',' ')
        obj['joinnum']=i.joinnum
        obj['isvote'] =i.isvote
        if i.isvote:
            data_list.insert(0,obj)
        else:
            data_list.append(obj)
    return JsonResponse({'status':1,'data':data_list})

def theactivety(request):
    userid = request.POST.get('userid')
    print('>>>>>userid',userid)
    activetyid = int(request.POST.get('activetyid'))
    #是否已经关注
    if userid is not None:
        isjoin = Join.objects.filter(Q(userid =userid)&Q(activety_id = activetyid))
        isjoin = True if isjoin.exists() else False
    else:
        isjoin = False
    activety = Activety.objects.get(id=activetyid)
    endtime = activety.endtime
    if activety.getprize_userid != '':
        getprize_nickname = activety.getprize_nickname
        isend = True
    else:
        endstamp = floor(time.mktime(endtime.timetuple()))
        now = ceil(time.time())
        isend = False if now - endstamp < 0 else  True
        if isend is True:
            joins = Join.objects.filter(activety_id = activetyid)
            user_list = [(i.userid,i.username) for i in joins]
            if user_list:
                getprize = random.choice(user_list)
                getprize_nickname = getprize[1]
                activety.getprize_nickname = getprize[1]
                activety.getprize_userid = getprize[0]
                activety.save()
            else:getprize_nickname = ''
        else:
            getprize_nickname = ''
    thedata = {}
    activety_joinnum= activety.joinnum
    thedata['img'] = activety.img
    thedata['id'] = activety.id
    thedata['name'] = activety.name
    thedata['support'] = activety.support
    thedata['endtime'] = str(endtime)[:19].replace('T',' ')
    thedata['joinnum'] = activety_joinnum
    thedata['explain'] = activety.explain
    thedata['isvote'] = activety.isvote
    thedata['isjoin'] = isjoin
    thedata['isend'] = isend
    colorlist = ['#86B7F9','#FF95B3','#FF96B9','#8ED673','#BF9DFE']
    thedata['getprize_nickname'] = [] if getprize_nickname == '' else [{'name':getprize_nickname,'color':random.choice(colorlist)}]
    join_names = activety.join_set.all().order_by('time')
    # 参与人列表
    join_detail = []
    if join_names.exists():
        for i in join_names:
            obj = {}
            obj['username'] = i.username
            obj['time'] = i.time
            obj['color'] = random.choice(colorlist)
            join_detail.insert(0,obj)
    thedata['join_detail'] = join_detail
    #投票数据列表
    vote_list = []
    if activety.isvote:
        votes = Vote.objects.filter(activety_id = activetyid)
        for vote in votes:
            obj = {}
            chooseid = vote.id
            choosename = vote.choose
            num = vote.num
            percent = "0%" if activety_joinnum==0 else'%.2f%%'%(num/activety_joinnum*100)
            obj['chooseid'] =chooseid
            obj['choosename'] = choosename
            obj['num'] = num
            obj['percent'] = percent
            vote_list.append(obj)
    thedata['vote_detail'] = vote_list
    return JsonResponse({'status':1,'data':thedata})


def join(request):
    userid = request.POST.get('userid')
    activety = int(request.POST.get('activetyid'))
    chooseid = request.POST.get('chooseid')
    user = User.objects.get(userid = userid)
    theactivety = Activety.objects.get(id = activety)
    join,err = Join.objects.get_or_create(activety = theactivety,userid = user.userid,username = user.nickName)
    if err:
        if theactivety.isvote:
            if chooseid is None:
                return JsonResponse({'status': 0,'code':'未上传投票参数'})
            voto = Vote.objects.get(id=int(chooseid))
            voto.num += 1
            voto.save()
        theactivety.joinnum += 1
        theactivety.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status': 1,'code':'he was voted'})


#我参加的活动
def myjoin(request):
    userid = request.POST.get('userid')
    joins = Join.objects.filter(userid = userid)
    data_list = []
    if joins.exists():
        for join in joins:
            activety = join.activety
            obj = {}
            obj['img'] = activety.img
            obj['id'] = activety.id
            obj['name'] = activety.name
            obj['support'] = activety.support
            obj['endtime'] = str(activety.endtime)[:19].replace('T',' ')
            obj['joinnum'] = activety.joinnum
            data_list.append(obj)
    return JsonResponse({'status': 1, 'data': data_list})

#我中奖的活动
def myprize(request):
    userid = request.POST.get('userid')
    activeties = Activety.objects.filter(getprize_userid = userid)
    data_list = []
    if activeties.exists():
        for i in activeties:
            obj = {}
            obj['img'] = i.img
            obj['id'] = i.id
            obj['name'] = i.name
            obj['support'] = i.support
            obj['endtime'] = i.endtime
            obj['joinnum'] = i.joinnum
            data_list.append(obj)
    return JsonResponse({'status': 1, 'data': data_list})

def mycoupon(request):
    userid = request.POST.get('userid')
    coupons = Usercoupon.objects.filter(userid=userid)
    data = []
    if coupons.exists():
        for coupon in coupons:
            thecoupon = {}
            thecoupon['name'] = coupon.coupon.name
            thecoupon['num'] = coupon.coupon.num
            thecoupon['img'] = coupon.coupon.img
            thecoupon['time'] = coupon.coupon.time
            thecoupon['type'] = coupon.coupon.type
            data.append(thecoupon)
    return JsonResponse({'status': 1, 'data': data})


def getcoupon(request):
    userid = request.POST.get('userid')
    type = int(request.POST.get('type'))
    coupons = Usercoupon.objects.filter(userid=userid)
    data = []
    if coupons.exists():
        for coupon in coupons:
            endtime = coupon.coupon.time
            end = time.mktime(endtime.timetuple())
            now = time.time()
            if coupon.coupon.type == type and now < end:
                thecoupon = {}
                thecoupon['name']= coupon.coupon.name
                thecoupon['num']= coupon.coupon.num
                thecoupon['img']=coupon.coupon.img
                thecoupon['time']= coupon.coupon.time
                thecoupon['id']= coupon.coupon.id
                data.append(thecoupon)
            elif now > end:
                coupon.delete()
    return JsonResponse({'status': 1, 'data': data})
