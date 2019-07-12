
import hashlib
import random
import time

from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# Create your views here.
from activety.models import Usercoupon, Coupon
from news.models import *
from paly.logic_getdata_fromweixn import *
from paly.models import *


def helloword(request):
    print(1)
    return HttpResponse('hello world')


# 测试连接
def getid(request):
    #测试与微信后台连接
    if request.method == 'GET':
        echostr = request.GET.get('echostr')
        return HttpResponse(echostr)


def generate_token():
    token = str(time.time()) + str(random.random())
    # md5算法
    md5 = hashlib.md5()
    md5.update(token.encode('utf-8'))

    token = md5.hexdigest()

    return token


def getuser(request):
    encryptedData = request.POST.get('encryptedData')
    iv = request.POST.get('iv')
    code = request.POST.get('code')
    d = get_unionid(code)
    errcode = d.get("errcode")
    if errcode:
        errmsg =d.get("errmsg")
        send_data = dict(status = 0,errcode =errcode,errmsg =errmsg)
        return JsonResponse(send_data)
    else:
        openId = d["openid"]

        # 存储用户信息
        user = User.objects.filter(pk=openId)
        if not user.exists():
            session_key = d["session_key"]
            user_data = getuserdata(session_key, encryptedData, iv)
        # """
        # 参考数据
        # {'openId': 'o3S7I5VDKwKP2005blNM92uRwaQk', 'nickName': '乐～', 'gender': 1,
        # 'language': 'zh_CN', 'city': 'Yueyang', 'province': 'Hunan', 'country': 'China',
        # 'avatarUrl': 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKABUOialWDJn5O8LzCXjySvRF7xnTE6Xv4czhKUyT1Qb04QAzic3amCfZGoBwCafepvFZ7YmcXCpeQ/132',
        #  'unionId': 'o2o3m1HOuzMP5yEX0X2uxBzNPWC0', 'watermark': {'timestamp': 1554208372, 'appid': 'wxc50f63e5b68a91f4'}}
            nickName = user_data.get('nickName')
            gender = user_data.get('gender')
            language = user_data.get('language')
            city = user_data.get('city')
            province = user_data.get('province')
            country = user_data.get('country')
            avatarUrl = user_data.get('avatarUrl')
            unionId = user_data.get('unionId')
            token = generate_token()
            userid = openId + str(random.randint(333, 667))


            user = User()
            user.userid = userid
            user.openId =openId
            user.nickName =nickName
            user.gender = gender
            user.language = language
            user.city = city
            user.province = province
            user.country = country
            user.avatarUrl = avatarUrl
            user.unionId = unionId
            user.token = token
            user.save()

            #登录即送优惠券
            cous = Coupon.objects.all()
            for cou in cous:
                usercou = Usercoupon()
                usercou.userid = userid
                usercou.coupon = cou
                usercou.save()
        else:
            user = user[0]
            userid = user.userid
            token = user.token
            nickName = user.nickName
            gender = user.gender
            language = user.language
            avatarUrl = user.avatarUrl

        post_num = user.post_num
        concern_num = user.concern_num
        fans_num = user.fans_num
        experience = user.experience

        send_data={
            "status":1,
            "user_data":{
                "userid":userid,
                "token":token,
                "nickName":nickName,
                "gender":gender,
                "language":language,
                "avatarUrl":avatarUrl,
                'experience':experience,
                'post_num':post_num,
                'concern_num':concern_num,
                'fans_num':fans_num
            }
        }
        return  JsonResponse(send_data)


def go_mine(request):
    token = request.POST.get('token')
    user =  User.objects.get(token=token)
    userid = user.userid
    token = user.token
    nickName = user.nickName
    gender = user.gender
    language = user.language
    avatarUrl = user.avatarUrl
    experience = user.experience
    post_num = user.post_num
    concern_num = user.concern_num
    fans_num = user.fans_num
    send_data = {
        "status": 1,
        "user_data": {
            "userid": userid,
            "token": token,
            "nickName": nickName,
            "gender": gender,
            "language": language,
            "avatarUrl": avatarUrl,
            'experience': experience,
            'post_num': post_num,
            'concern_num': concern_num,
            'fans_num': fans_num,
        }
    }
    return JsonResponse(send_data)

def notreadnews(request):
    userid = request.POST.get('userid')
    notread = Main_comment.objects.filter(
        Q(to_man=userid) & Q(main_isread=0)).count() | Good_num_tiezi.objects.filter(
        Q(get_good_man=userid) & Q(isread=0)&Q(isdelete =0)).count()| Side_comment.objects.filter(
        Q(to_man=userid) & Q(side_isread=0)).count() | Good_num_maincomment.objects.filter(
        Q(get_good_man=userid)&Q(isread=0)&Q(isdelete =0)).count()
    if notread != 0:
        notread = 1
    return JsonResponse({'status':notread})

#浏览用户详情
def browseuserdata(request):
    theuserid = request.POST.get('theuserid')
    togetuserid = request.POST.get('togetuserid')
    print('>>>>>',theuserid,togetuserid)
    # 展示用户详情
    user = User.objects.filter(userid=togetuserid)[0]
    nickName = user.nickName
    gender = user.gender
    avatarUrl = user.avatarUrl
    experience = user.experience
    post_num = user.post_num
    concern_num = user.concern_num
    fans_num = user.fans_num
    userid = user.userid
    # 是否已经关注
    isfocoused = Concern.objects.filter(Q(userid = theuserid) & Q(concern_userid = togetuserid))
    focoused = 1 if isfocoused.exists() else 0

    tiezis = News.objects.filter(userid=togetuserid,isdelete = 0).order_by('good_num')[0:5]
    if tiezis.exists():
        tiezis_data = []
        for tiezi in tiezis:
            obj = {}
            obj['title'] = tiezi.title
            obj['id'] = tiezi.id
            obj['content'] = tiezi.content
            obj['time'] = str(tiezi.time)[:19].replace('T',' ')
            obj['img1'] = tiezi.img1
            obj['top'] = tiezi.top
            obj['comment_num'] = tiezi.comment_num
            obj['good_num'] = tiezi.good_num
            tiezis_data.append(obj)
    else:
        tiezis_data = []
    send_data = {
        "status": 1,
        "user_data": {
            "userid": userid,
            "nickName": nickName,
            "gender": gender,
            "avatarUrl": avatarUrl,
            'experience': experience,
            'post_num': post_num,
            'concern_num': concern_num,
            'fans_num': fans_num,
            'focoused': focoused
        },
        "tiezi_data": tiezis_data
    }
    return JsonResponse(send_data)

#关注
def concern(request):
    userid = request.POST.get('userid')
    concern_userid = request.POST.get('concern_userid')
    user = User.objects.filter(userid=userid)[0]
    user.concern_num += 1
    user.save()

    concern_user = User.objects.filter(userid=concern_userid)[0]
    concern_user.fans_num += 1
    concern_user.save()

    concern = Concern()
    concern.userid = userid
    concern.concern_userid = concern_userid
    concern.concern = concern_user
    concern.save()

    fans = Fans()
    fans.userid = concern_userid
    fans.fans_userid = userid
    fans.fans = user
    fans.save()
    return JsonResponse({'statu':1})

#取消关注
def no_concern(request):
    userid = request.POST.get('userid')
    concern_userid = request.POST.get('concern_userid')
    user = User.objects.filter(userid=userid)[0]
    user.concern_num -= 1
    user.save()
    concern_user = User.objects.filter(userid=concern_userid)[0]
    concern_user.fans_num -= 1
    concern_user.save()
    concern = Concern.objects.filter(Q(userid=userid)& Q(concern=concern_user))
    concern.delete()
    fans = Fans.objects.filter(Q(userid=concern_userid)& Q(fans=user))
    fans.delete()
    return JsonResponse({'statu':1})

def myconcern(request):
    userid = request.POST.get('userid')
    concerns = Concern.objects.filter(userid=userid)
    concernsdata = []
    if concerns.exists():
        for concern in concerns:
            user = concern.concern
            userdata = {}
            userdata['userid'] = user.userid
            userdata['nickName'] = user.nickName
            userdata['avatarUrl'] = user.avatarUrl
            userdata['gender'] = user.gender
            userdata['hidden'] = False
            concernsdata.append(userdata)
    return JsonResponse({'data':concernsdata})

def myfans(request):
    userid = request.POST.get('userid')
    fans = Fans.objects.filter(userid=userid)
    fansdata = []
    if fans.exists():
        for thefans in fans:
            user = thefans.fans
            userdata = {}
            userdata['userid'] = user.userid
            userdata['nickName'] = user.nickName
            userdata['avatarUrl'] = user.avatarUrl
            userdata['gender'] = user.gender
            fansdata.append(userdata)
    return JsonResponse({'data':fansdata})

