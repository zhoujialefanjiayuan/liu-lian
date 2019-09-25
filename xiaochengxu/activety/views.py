import time
from math import floor, ceil

from django.core.cache import cache
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
from vocal_concert.models import Singger_img, Vocal


#@cache_page(60*5,cache='longtime')
def allactivety(request):
    #抽奖 助力 投票
    type = request.GET.get('type')
    if type == '1':
        activeties = Activety.objects.filter(isvote=0,zhuli_target=0).order_by('-endtime')
    elif type == '2':
        activeties = Activety.objects.filter(zhuli_target__gt=0).order_by('-endtime')
    else :
        activeties = Activety.objects.filter(isvote=1).order_by('-endtime')
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
        obj['zhuli_target'] =i.zhuli_target
        data_list.append(obj)
    return JsonResponse({'status':1,'data':data_list})

def addvote(request):
    userid = request.POST.get('userid')
    activetyid = int(request.POST.get('activetyid'))
    choose = request.POST.get('choose')
    Addvote.objects.get_or_create(userid=userid,activetyid=activetyid,choose=choose)
    num = Addvote.objects.filter(choose=choose).count()
    return JsonResponse({'choose': choose,
     'num': num,
     'basenum': 100})

def theactivety(request):
    userid = request.POST.get('userid')
    activetyid = request.POST.get('activetyid')
    #是否已经关注
    if userid is not None:
        isjoin = Join.objects.filter(Q(userid =userid)&Q(activety_id = activetyid))
        isjoin = True if isjoin.exists() else False
    else:
        isjoin = False
    activety = Activety.objects.get(id=activetyid)
    endtime = activety.endtime
    if activety.getprize_nickname != '':
        if activety.getprize_nickname != 'noneprize_foractivety':
            getprize_nickname = activety.getprize_nickname.split(',')
        else:
            getprize_nickname = 'noneprize_foractivety'
        isend = True
    else:
        endstamp = floor(time.mktime(endtime.timetuple()))
        now = ceil(time.time())
        isend = False if now - endstamp < 0 else  True
        if isend is True:
            if activety.getprize_num != 0:
                joins = Join.objects.filter(activety_id=activetyid)
                user_list = [(i.userid,i.username) for i in joins]
                if user_list:
                    getprize = random.sample(user_list,k=activety.getprize_num)
                    getprize_nickname = []
                    getprize_userid =[]
                    for i in getprize:
                        getprize_nickname.append(i[1])
                        getprize_userid.append(i[0])
                    activety.getprize_nickname = ','.join(getprize_nickname)
                    activety.getprize_userid = ','.join(getprize_userid)
                    activety.save()
                else:
                    activety.getprize_nickname = 'noneprize_foractivety'
                    activety.save()
            else:
                activety.getprize_nickname = 'noneprize_foractivety'
                activety.save()
        else:
            getprize_nickname =[]
    thedata = {}
    adtab = {}
    adtab['logurl']= activety.logurl
    adtab['weburl']= activety.weburl
    adtab['appid'] = activety.appid
    adtab['apppage']  = activety.apppage
    adtab['navigatetotype']= 1 if activety.weburl == '' else 0
    thedata['adtab'] = adtab
    activety_joinnum= activety.joinnum
    thedata['img'] = activety.img
    thedata['id'] = activety.id
    thedata['name'] = activety.name
    thedata['support'] = activety.support
    thedata['endtime'] = str(endtime)[:19].replace('T',' ')
    thedata['joinnum'] = activety_joinnum
    thedata['explain'] = activety.explain
    thedata['isvote'] = activety.isvote
    thedata['zhuli_target'] = activety.zhuli_target
    thedata['isjoin'] = isjoin
    thedata['isend'] = isend
    colorlist = ['#86B7F9','#FF95B3','#FF96B9','#8ED673','#BF9DFE']
    #获奖名单
    getprize_nickname_send = []
    if getprize_nickname != 'noneprize_foractivety':
        for i in getprize_nickname:
            obj = {}
            obj['name'] = i
            obj['color'] = random.choice(colorlist)
            getprize_nickname_send.append(obj)
            thedata['getprize_nickname'] = getprize_nickname_send
    else:
        thedata['getprize_nickname'] = []
    join_names = activety.join_set.order_by('-id').all()
    cache.set('join_name'+ activetyid,join_names,10)
    # 参与人列表
    thedata['join_more'] = 1 if len(join_names)>16 else 0
    join_detail = []
    if join_names.exists():
        for i in join_names[:16]:
            obj = {}
            obj['username'] = i.username
            obj['time'] = str(i.time)
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
    #添加城市的选项
    if activetyid == '2':
        choose = Addvote.objects.filter(userid=userid)
        if  choose.exists():
            choosename = choose[0].choose
            num = Addvote.objects.filter(choose=choosename).count()
            basenum = 100
            thedata['choosedata'] = {'choose':choosename,
                                     'num':num,
                                     'basenum':basenum}
            thedata['add_choose'] = True
            thedata['isaddchoose'] = True
            if num >= basenum:
                Vote.objects.get_or_create(activety=activety,num=num,choose=choosename)
        else:
            thedata['add_choose'] = True
            thedata['choosedata'] = {}
            thedata['isaddchoose'] = False
    else:
        thedata['add_choose'] = False
        thedata['choosedata'] = {}
        thedata['isaddchoose'] = False
        #助力数据列表
    zhuli_list= []
    if activety.zhuli_target:
        zhuli_targets = Zhouli_stage.objects.filter(activety_id = activetyid)
        for zhuli_target in  zhuli_targets:
            stage= to_dict(zhuli_target)
            stage['percent'] = str(stage['percent']) + '%'
            zhuli_list.append(stage)
    thedata['zhuli_list'] = zhuli_list
    thedata['zhuli_percent'] = '%.2f%%'%((activety.joinnum / activety.zhuli_target)*100) if activety.zhuli_target !=0 else ''
    if activety.joinnum >= activety.zhuli_target:
        thedata['zhuli_percent'] = '100%'
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
    activeties = Activety.objects.filter(getprize_userid__contains = userid)
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


def isjoin(request):
    userid = request.POST.get('userid')
    activetyid = int(request.POST.get('activetyid'))
    isjoin = Join.objects.filter(Q(userid=userid) & Q(activety_id=activetyid))
    isjoin = True if isjoin.exists() else False
    return {'status':1,'isjoin':isjoin}


def show_joins(request):
    activetyid = request.GET.get('activetyid')
    page = int(request.GET.get('page'))
    if page > 6:
        page = random.randint(1,6)
    join_list = cache.get('join_name'+ activetyid)
    if join_list is None:
        join_list = Join.objects.filter(activety_id = int(activetyid)).order_by('-time')
        cache.set('join_name' + activetyid,join_list,10)
    list_data = []
    for i in join_list[(page-1)*100:page*100]:
        obj = {}
        obj['username'] = i.username
        obj['time'] = str(i.time)
        list_data.append(obj)
    return JsonResponse({'status': 1, 'data': list_data})


def indexswiper(request):
    swipers = Indexswiper.objects.all()
    swiper_data = [to_dict(i) for i in swipers]
    #热门活动
    activeties = Activety.objects.order_by('-endtime')[:2]
    activety_data = []
    for i in activeties:
        obj = {}
        obj['img'] = i.img
        obj['activetyid'] = i.id
        obj['endtime'] = str(i.endtime)[:19].replace('T',' ')
        obj['title'] = i.name
        activety_data.append(obj)
    return JsonResponse({'status': 1, 'swiper_data': swiper_data,'activety_data':activety_data})

def indexvocal(request):
    singgers = Singger_img.objects.all()
    singgers = random.sample([i.siggger_name for i in singgers],4)
    list_data = []
    for singger in singgers:
        obj = {}
        vocal = Vocal.objects.filter(singger=singger).order_by('-id')[0]
        obj['id'] = vocal.id
        obj['project_name'] = vocal.project_name
        obj['little_img'] = vocal.little_img
        obj['city'] = vocal.city
        obj['location'] = vocal.location
        list_data.append(obj)
    return JsonResponse({'status': 1, 'list_data': list_data})