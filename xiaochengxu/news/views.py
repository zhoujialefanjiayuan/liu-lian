import copy
from datetime import datetime
from itertools import chain

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.db.models import Q
from django.http import JsonResponse

from news.DFAfilter import *
from news.models import *

from paly.models import User
from paly.models import Concern
from xiaochengxu.settings import BASE_DIR


def to_dict(obj):
    '''将当前对象转换成字典'''
    attr_dict = {}
    for field in obj._meta.get_fields():
        try:
            name = field.attname  # 属性名
            value = getattr(obj, name)  # 属性值
            attr_dict[name] = value
        except:
            continue
    return attr_dict





#发表存储帖子
def write_news(request):
    userid = request.POST.get('userid')
    title = request.POST.get('title')
    content = request.POST.get('content')
    only_title = userid + title
    #过滤内容
    gfw = cache.get('gfw')
    if gfw is None:
        gfw = DFAFilter()
        gfw.parse(BASE_DIR + '/news/DFAfilter/keywords')
        cache.set('gfw',gfw,100)
    content = gfw.filter(content,'*')
    title = gfw.filter(title,'*')

    img1 = request.POST.get('img1')
    img2= request.POST.get('img2')
    img3 = request.POST.get('img3')

    # 判断是否重复发帖
    isduplity=News.objects.filter(only_title = only_title,isdelete=0)
    if isduplity.exists():
        data = {'status': 0, 'code': '标题已重复不可用，请更换标题或在标题尾部添加数字以区分'}
        return JsonResponse(data)
    else:
        new = News()
        new.userid= userid
        new.title =title
        new.content=content
        new.only_title = only_title
        new.img1=img1
        new.img2=img2
        new.img3=img3
        new.save()
        user = User.objects.get(userid=userid)
        user.experience += 10
        user.post_num += 1
        user.save()
        return JsonResponse({'status':1,'code':'发贴成功'})



#首页帖子社区问答展示
def indexshow_news(requset):
    # hours_for24 = 86400
    # now = get_time()
    # begin = now -hours_for24*60
    index_news = News.objects.filter(pk__lt=100)
    list_data=[]
    for news in index_news:
        obj = {}
        one = to_dict(news)
        one['tiezi_id'] = one.pop('id')
        one.pop('only_title')
        obj['tiezi_data'] =one

        openId = news.userid[:-3]
        user = User.objects.get(openId = openId)
        tow = {}
        tow['userid'] = user.userid
        tow['nickName'] = user.nickName
        tow['avatarUrl'] = user.avatarUrl
        tow['gender'] = user.gender

        obj['user'] = tow
        list_data.append(obj)

    data = {'status': 1,
            'index_news': list_data
            }
    return JsonResponse(data)

#首页帖子精选帖子展示
def choiceness_news(requset):

    index_news = News.objects.filter(good_num__gte=200)
    list_data = []
    for news in index_news:
        obj = {}
        one = to_dict(news)
        one['tiezi_id'] = one.pop('id')
        one.pop('only_title')
        obj['tiezi_data'] = one

        openId = news.userid[:-3]
        user = User.objects.get(openId=openId)
        tow = {}
        tow['userid'] = user.userid
        tow['nickName'] = user.nickName
        tow['avatarUrl'] = user.avatarUrl
        tow['gender'] = user.gender

        obj['user'] = tow
        list_data.append(obj)

    data = {'status': 1,
            'index_news': list_data
            }
    return JsonResponse(data)


#社区搜索帖子
def search(request):
    keyword = request.GET.get('keyword')
    index_news = News.objects.filter(title__contains=keyword,isdelete = 0).order_by('-comment_num')
    list_data = []
    for news in index_news:
        obj = {}
        one = to_dict(news)
        one['tiezi_id'] = one.pop('id')
        one['time'] = str(one['time'])[:19].replace('T',' ')
        one.pop('only_title')
        obj['tiezi_data'] = one

        openId = news.userid[:-3]
        user = User.objects.get(openId=openId)
        tow = {}
        tow['userid'] = user.userid
        tow['nickName'] = user.nickName
        tow['avatarUrl'] = user.avatarUrl
        tow['gender'] = user.gender

        obj['user'] = tow
        list_data.append(obj)

    data = {'status': 1,
            'index_news': list_data
            }
    return JsonResponse(data)

#榜单帖子,page<=5
#@cache_page(60)
def topnews(request):
    page = request.GET.get('page')
    page = int(page)
    sum_news = cache.get('sum_news')
    if sum_news == None:
        thetop = News.objects.filter(top=1,isdelete = 0)
        allnews = News.objects.filter(top=0,isdelete = 0).order_by('-time')
        nownews = allnews[:5]
        commentnews = sorted(allnews[5:],key=lambda item : item.comment_num,reverse=True)
        sum_news = list(chain(thetop,nownews,commentnews))
        cache.set('sum_news', sum_news,5)
    toshownews = sum_news[(page-1)*25:page*25]
    list_data = []
    for thenews in toshownews:
        obj = {}
        tiezi = to_dict(thenews)
        tiezi['time'] = str(tiezi['time'])[:19].replace('T',' ')
        openId = tiezi['userid'][:-3]
        user = User.objects.get(openId=openId)
        tow = {}
        tow['userid'] = user.userid
        tow['nickName'] = user.nickName
        tow['avatarUrl'] = user.avatarUrl
        tow['gender'] = user.gender
        obj['user'] = tow
        obj['tiezi'] = tiezi
        list_data.append(obj)
    return JsonResponse({'status':1,'data':list_data})


def recomend_news(request):
    pass


#关注的帖子
def focousenews(request):
    userid = request.POST.get('userid')
    page = int(request.POST.get('page'))
    concerns = Concern.objects.filter(userid=userid)
    list_data = []
    for concern in concerns:
        concern_userid = concern.concern_userid
        user = concern.concern
        user_data = {}
        user_data['userid'] = user.userid
        user_data['nickName'] = user.nickName
        user_data['avatarUrl'] = user.avatarUrl
        user_data['gender'] = user.gender
        tiezis = News.objects.filter(userid = concern_userid)
        for tiezi in  tiezis:
            obj = {}
            tiezi_data = to_dict(tiezi)
            tiezi_data['time'] = str(tiezi_data['time'])[:19].replace('T',' ')
            obj['user'] = user_data
            obj['tiezi'] = tiezi_data
            list_data.append(obj)
    if page < 2:
        list_data = sorted(list_data,key=lambda t:t['tiezi']['time'],reverse=True)[0:100]
    else:
        list_data = sorted(list_data, key=lambda t: t['tiezi']['time'], reverse=True)[(page-1)*100:page*100]
    return JsonResponse({'status':1,'data':list_data})


#轮播图帖子 id必须与数据库中所有帖子id一致
@cache_page(60*60,cache='longtime')
def swipper(request):
    index_news = News.objects.filter(isswiper = 1,isdelete = 0)
    list_data = []
    for news in index_news:
        obj = {}
        one = to_dict(news)
        one['tiezi_id'] = one.pop('id')
        one.pop('only_title')
        obj['tiezi_data'] = one
        openId = news.userid[:-3]
        user = User.objects.get(openId=openId)
        tow = {}
        tow['userid'] = user.userid
        tow['nickName'] = user.nickName
        tow['avatarUrl'] = user.avatarUrl
        tow['gender'] = user.gender
        obj['user'] = tow
        list_data.append(obj)

    data = {'status': 1,
            'index_news': list_data
            }
    return JsonResponse(data)


#主评论
def main_comment(request):
    # tiezi_id = models.IntegerField()
    # main_openor = models.CharField(max_length=50)  # openId
    # com_content = models.TextField(max_length=512)
    # good_num = models.IntegerField(default=0)
    # to_man = models.CharField(max_length=50)  # 发表帖子的人openId
    # main_isread = models.BooleanField(default=0)

    tiezi_id = int(request.POST.get('tiezi_id'))
    main_openor = request.POST.get('main_openor')
    to_man = request.POST.get('to_man')
    com_content = request.POST.get('com_content')

    gfw = cache.get('gfw')
    if gfw is None:
        gfw = DFAFilter()
        gfw.parse(BASE_DIR + '/news/DFAfilter/keywords')
        cache.set('gfw', gfw, 100)
    com_content = gfw.filter(com_content, '*')

    #如果评论自己的帖子，显示已读
    if main_openor == to_man:
        comment = Main_comment.objects.get_or_create(tiezi_id=tiezi_id, main_openor=main_openor,
                                                     com_content=com_content, to_man=to_man,main_isread=1)
    else:
        comment = Main_comment.objects.get_or_create(tiezi_id = tiezi_id,main_openor = main_openor,com_content = com_content,to_man = to_man)

    if False in comment:
       return JsonResponse({'status': 0, 'code': '不可评论相同内容'})
    else:
        # 评论数加1
        tiezi = News.objects.get(id=tiezi_id)
        tiezi.comment_num += 1
        tiezi.save()
        return JsonResponse({'status': 1, 'code': '主评论成功'})


# 副评论
def side_comment(request):
    # main_comment_id = models.IntegerField()
    # side_openor = models.CharField(max_length=50)  # openId
    # side_com_content = models.TextField(max_length=512)
    # to_man = models.CharField(max_length=50)  # 发表主评论的人openId
    # side_isread = models.BooleanField(default=0)

    main_comment_id = int(request.POST.get('main_comment_id'))
    tiezi_id = int(request.POST.get('tiezi_id'))
    side_openor = request.POST.get('side_openor')
    to_man = request.POST.get('to_man')
    side_com_content = request.POST.get('side_com_content')
    gfw = cache.get('gfw')
    if gfw is None:
        gfw = DFAFilter()
        gfw.parse(BASE_DIR + '/news/DFAfilter/keywords')
        cache.set('gfw', gfw, 100)
    side_com_content = gfw.filter(side_com_content, '*')
    if side_openor == to_man:
        comment = Side_comment.objects.get_or_create(main_comment_id=main_comment_id, side_openor=side_openor,
                                                     tiezi_id=tiezi_id, to_man=to_man,side_isread=1,
                                                     side_com_content=side_com_content)
    else:
        comment = Side_comment.objects.get_or_create(main_comment_id = main_comment_id,side_openor = side_openor,tiezi_id = tiezi_id,to_man = to_man,side_com_content = side_com_content)

    if False in comment:
        return JsonResponse({'status': 0, 'code': '不可重复回复相同内容'})
    else:
        # 帖子评论数加1
        tiezi = News.objects.get(id=tiezi_id)
        tiezi.comment_num += 1
        tiezi.save()
        #更新主评论时间
        maincomment = Main_comment.objects.get(pk=main_comment_id)
        print(comment[0].opentime > maincomment.updatetime)
        if comment[0].opentime > maincomment.updatetime:

            maincomment.updatetime= comment[0].opentime
            maincomment.save()
        return JsonResponse({'status': 1, 'code': '副评论成功'})



#展示帖子详情
def show_detail(request):
    tiezi_id = request.POST.get('id')
    userid = request.POST.get('userid')

    # print("接收参数",tiezi_id,userid)
    obj = {}
    news = News.objects.get(id=tiezi_id)
    tiezi_data = {}
    tiezi_data['tiezi_id'] = news.id
    user=news.userid
    tiezi_data['userid'] = user
    tiezi_data['title'] = news.title
    tiezi_data['img1'] = news.img1
    tiezi_data['img2'] = news.img2
    tiezi_data['img3'] = news.img3
    tiezi_data['time'] = str(news.time)[:19].replace('T',' ')
    tiezi_data['content'] = news.content

    # 判断当前用户是否点赞主贴
    isgood_forTiezi = Good_num_tiezi.objects.filter(Q(tiezi_id=tiezi_id) & Q(make_good_man=userid)& Q(isdelete=0))
    if isgood_forTiezi.exists():
        tiezi_data['isgood_forTiezi'] = 1
    else:
        tiezi_data['isgood_forTiezi'] = 0

    #判断是否收藏该帖子
    iscollect_forTiezi = Collect_tiezi.objects.filter(Q(tiezi_id=tiezi_id) & Q(collector=userid))
    if iscollect_forTiezi.exists():
        tiezi_data['iscollect_forTiezi'] = 1
    else:
        tiezi_data['iscollect_forTiezi'] = 0

    writor = User.objects.get(openId=user[:-3])
    tiezi_data['writor_nikename'] = writor.nickName
    tiezi_data['writor_avatarUrl'] = writor.avatarUrl
    obj['tiezi_data'] = tiezi_data
    return  JsonResponse({'status': 1, 'data': obj})


def onepage(request):
    page = int(request.GET.get('page'))
    tiezi_id = int(request.GET.get('tiezi_id'))
    userid = request.GET.get('userid')
    maincomments = Main_comment.objects.filter(tiezi_id=tiezi_id).order_by('-updatetime')
    main_list = []
    for maincomment in maincomments[(page-1)*25:page*25]:
        main_data = {}
        mian_id = maincomment.id
        main_data['id'] = mian_id
        main_data['com_content'] = maincomment.com_content
        main_data['good_num'] = maincomment.good_num
        main_data['tiezi_id'] = maincomment.tiezi_id
        main_data['opentime'] = str(maincomment.opentime)[:19].replace('T',' ')
        main_user = maincomment.main_openor
        main_data['main_openor'] = main_user
        Mainuser = User.objects.get(openId=main_user[:-3])
        main_data['from_main_nickname'] = Mainuser.nickName
        main_data['from_main_avatarurl'] = Mainuser.avatarUrl

        isgood = Good_num_maincomment.objects.filter(
            Q(main_comment_id=mian_id) & Q(make_good_man=userid) & Q(isdelete=0))
        if isgood.exists():
            main_data['isgood_forcomment'] = 1
        else:
            main_data['isgood_forcomment'] = 0

        sidecomments = Side_comment.objects.filter(main_comment_id=mian_id).order_by('-id')
        side_list = []
        for sidecomment in sidecomments:
            side_data = {}
            side_data['main_comment_id'] = sidecomment.main_comment_id
            side_data['id'] = sidecomment.id
            side_data['tiezi_id'] = sidecomment.tiezi_id
            side_data['side_com_content'] = sidecomment.side_com_content

            sideopenor = sidecomment.side_openor
            side_data['side_openor'] = sideopenor
            Sideopenor = User.objects.get(openId=sideopenor[:-3])
            side_data['from_side_nickname'] = Sideopenor.nickName
            sidecommentz_to_man = sidecomment.to_man
            side_data['sidecomment_to_man'] = sidecommentz_to_man
            Sidecommentz_to_man = User.objects.get(openId=sidecommentz_to_man[:-3])
            side_data['to_side_nickname'] = Sidecommentz_to_man.nickName

            side_list.append(side_data)

        main_data['sidecomments'] = side_list
        main_list.append(main_data)
    return JsonResponse({'status':1,'data':main_list})


def topcomments(request):
    tiezi_id = int(request.GET.get('tiezi_id'))
    userid = request.GET.get('userid')
    topcomments = Main_comment.objects.filter(Q(tiezi_id=tiezi_id) & Q(good_num__gte=100))
    top_list = []
    for maincomment in topcomments[:20]:
        main_data = {}
        mian_id = maincomment.id
        main_data['id'] = mian_id
        main_data['com_content'] = maincomment.com_content
        main_data['good_num'] = maincomment.good_num
        main_data['tiezi_id'] = maincomment.tiezi_id
        main_data['opentime'] = str(maincomment.opentime)[:19].replace('T',' ')
        main_user = maincomment.main_openor
        main_data['main_openor'] = main_user
        Mainuser = User.objects.get(openId=main_user[:-3])
        main_data['from_main_nickname'] = Mainuser.nickName
        main_data['from_main_avatarurl'] = Mainuser.avatarUrl

        isgood = Good_num_maincomment.objects.filter(
            Q(main_comment_id=mian_id) & Q(make_good_man=userid) & Q(isdelete=0))
        if isgood.exists():
            main_data['isgood_forcomment'] = 1
        else:
            main_data['isgood_forcomment'] = 0
        sidecomments = Side_comment.objects.filter(main_comment_id=mian_id).order_by('-id')
        side_list = []
        for sidecomment in sidecomments:
            side_data = {}
            side_data['main_comment_id'] = sidecomment.main_comment_id
            side_data['id'] = sidecomment.id
            side_data['tiezi_id'] = sidecomment.tiezi_id
            side_data['side_com_content'] = sidecomment.side_com_content

            sideopenor = sidecomment.side_openor
            side_data['side_openor'] = sideopenor
            Sideopenor = User.objects.get(openId=sideopenor[:-3])
            side_data['from_side_nickname'] = Sideopenor.nickName
            sidecommentz_to_man = sidecomment.to_man
            side_data['sidecomment_to_man'] = sidecommentz_to_man
            Sidecommentz_to_man = User.objects.get(openId=sidecommentz_to_man[:-3])
            side_data['to_side_nickname'] = Sidecommentz_to_man.nickName
            side_list.append(side_data)
        main_data['sidecomments'] = side_list
        top_list.append(main_data)
    return JsonResponse({'status': 1, 'data': top_list})

#帖子点赞
def good_fortiezi(request):
    tiezi_id = int(request.POST.get('tiezi_id'))
    make_good_man = request.POST.get('make_good_man')
    news = News.objects.get(pk=tiezi_id)
    get_good_man = news.userid
    #点赞自己显示已读
    if make_good_man == get_good_man:
        good_num_tiezi = Good_num_tiezi.objects.get_or_create(tiezi_id=tiezi_id,make_good_man=make_good_man,get_good_man=get_good_man,isread=1)

    else:
        good_num_tiezi= Good_num_tiezi.objects.get_or_create(tiezi_id=tiezi_id,make_good_man=make_good_man,get_good_man=get_good_man)
    if good_num_tiezi[1] == True:
        news.good_num += 1
        news.save()
    else:
        if good_num_tiezi[0].isdelete == 1:
            news.good_num += 1
            news.save()
    if good_num_tiezi[0].isdelete == 1:
        good_num_tiezi[0].isdelete = 0
        good_num_tiezi[0].save()
    return JsonResponse({'status': 1, 'code': '点赞成功','data':{'tiezi_id':tiezi_id}})

#取消点赞帖子
def delgood_fortiezi(request):
    tiezi_id = int(request.POST.get('tiezi_id'))
    userid= request.POST.get('make_good_man')
    goodfornews = Good_num_tiezi.objects.filter(make_good_man=userid,tiezi_id=tiezi_id)[0]
    if  goodfornews.isdelete == 0:
        goodfornews.isdelete = 1
        goodfornews.save()
        news = News.objects.get(pk=tiezi_id)
        news.good_num -= 1
        news.save()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})

#点赞主评论
def good_formiancomment(request):
    maincomment_id = int(request.POST.get('maincomment_id'))
    make_good_man = request.POST.get('make_good_man')

    maincomment = Main_comment.objects.get(pk=maincomment_id)
    get_good_man = maincomment.main_openor
    if make_good_man == get_good_man:
        good_num_maincomment = Good_num_maincomment.objects.get_or_create(main_comment_id=maincomment_id,
                                                                          make_good_man=make_good_man,
                                                                          get_good_man=get_good_man,isread =1)
    else:
        good_num_maincomment = Good_num_maincomment.objects.get_or_create(main_comment_id=maincomment_id, make_good_man=make_good_man,
                                                 get_good_man=get_good_man)
    if good_num_maincomment[1] == True:
        maincomment.good_num +=1
        maincomment.save()
    else:
        if good_num_maincomment[0].isdelete == 1:
            maincomment.good_num += 1
            maincomment.save()
    if good_num_maincomment[0].isdelete == 1:
        good_num_maincomment[0].isdelete = 0
        good_num_maincomment[0].save()
    return JsonResponse({'status': 1, 'code': '点赞成功', 'data': {'maincomment_id': maincomment_id}})

#取消点赞主评论
def delgood_formiancomment(request):
    maincomment_id = int(request.POST.get('maincomment_id'))
    make_good_man = request.POST.get('make_good_man')
    goodformaincomment = Good_num_maincomment.objects.filter(main_comment_id = maincomment_id,make_good_man =make_good_man)[0]
    if goodformaincomment.isdelete == 0:
        goodformaincomment.isdelete = 1
        goodformaincomment.save()
        maincomment = Main_comment.objects.get(pk=maincomment_id)
        maincomment.good_num -= 1
        maincomment.save()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})

#收藏帖子
def collect(request):
    collector = request.POST.get('collector')
    tiezi_id = request.POST.get('tiezi_id')
    collect =Collect_tiezi.objects.get_or_create(collector=collector,tiezi_id=tiezi_id)
    if False in collect:
        return JsonResponse({'status': 0, 'code': '已收藏该贴'})
    else:
        return JsonResponse({'status': 1, 'code': '收藏成功'})

#取消收藏
def delcollect(request):
    collector = request.POST.get('collector')
    tiezi_id = request.POST.get('tiezi_id')
    collect =Collect_tiezi.objects.filter(Q(collector=collector)&Q(tiezi_id=tiezi_id))
    if collect.exists():
        collect.delete()
        return JsonResponse({'status': 1, 'code': '取消收藏成功'})
    else:
        return JsonResponse({'status': 0, 'code': '请先收藏该贴'})


#举报接口
def report(request):
    id = request.POST.get('id')
    content = request.POST.get('content')
    try:
        re = Report()
        re.tiezi_id = int(id)
        re.content = content
        re.save()
        return  JsonResponse({'status': 1, 'code': '举报成功,后台人员正在受理'})
    except Exception as e:
        return JsonResponse({'status': 0, 'code': str(e)})


#我的收藏
def show_mycollect(request):
    userid = request.GET.get('userid')
    collects = Collect_tiezi.objects.filter(collector= userid)
    list_data = []
    if collects.exists():

        for collect in collects:
            tiezi_id = collect.tiezi_id
            thenews = News.objects.filter(id=tiezi_id,isdelete = 0)
            if thenews.exists() == False:
                continue
            news = thenews[0]
            obj = {}
            one = to_dict(news)
            one['tiezi_id'] = tiezi_id
            one['time'] = str(one['time'])[:19].replace('T',' ')
            one.pop('id')
            one.pop('only_title')
            obj['tiezi_data'] = one

            openId = news.userid[:-3]
            user = User.objects.get(openId=openId)
            tow = {}
            tow['userid'] = user.userid
            tow['nickName'] = user.nickName
            tow['avatarUrl'] = user.avatarUrl
            tow['gender'] = user.gender
            obj['user'] = tow

            list_data.append(obj)

        data = {'status': 1,
                'index_news': list_data
                }
        return JsonResponse(data)
    else:
        data = {'status': 0,
                'index_news': list_data
                }
        return JsonResponse(data)


#我的评论,只展示主评论
def show_mycomment(request):
    userid = request.GET.get('userid')
    comments = Main_comment.objects.filter(main_openor= userid)
    list_data = []
    if comments.exists():

        set_tiezi_id = set()
        #帖子去重
        for comment in comments:
            tiezi_id = comment.tiezi_id
            set_tiezi_id.add(tiezi_id)
        set_tiezi_id = sorted(set_tiezi_id, key=lambda x: x, reverse=True)
        for tiezi_id in set_tiezi_id:
            thenews = News.objects.filter(id=tiezi_id, isdelete=0)
            if thenews.exists() == False:
                continue
            obj = {}
            news = thenews[0]
            one = to_dict(news)
            one['tiezi_id'] = tiezi_id
            one['time'] = str(one['time'])[:19].replace('T', ' ')
            one.pop('id')
            one.pop('only_title')
            obj['tiezi_data'] = one

            openId = news.userid[:-3]
            user = User.objects.get(openId=openId)
            tow = {}
            tow['userid'] = user.userid
            tow['nickName'] = user.nickName
            tow['avatarUrl'] = user.avatarUrl
            tow['gender'] = user.gender
            obj['user'] = tow

            list_data.append(obj)

        data = {'status': 1,
                'index_news': list_data
                }
        return JsonResponse(data)
    else:
        data = {'status': 0,
                'index_news': list_data
                }
        return JsonResponse(data)

#我的点赞,只展示点赞的帖子
def show_mygood(request):
    userid = request.GET.get('userid')
    goods = Good_num_tiezi.objects.filter(make_good_man=userid,isdelete=0)
    list_data = []
    if goods.exists():
        for good in goods:
            tiezi_id = good.tiezi_id
            thenews = News.objects.filter(id=tiezi_id, isdelete=0)
            if thenews.exists() == False:
                continue
            obj = {}
            news = thenews[0]
            one = to_dict(news)
            one['tiezi_id'] = tiezi_id
            one['time'] = str(one['time'])[:19].replace('T', ' ')
            one.pop('id')
            one.pop('only_title')
            obj['tiezi_data'] = one

            openId = news.userid[:-3]
            user = User.objects.get(openId=openId)
            tow = {}
            tow['userid'] = user.userid
            tow['nickName'] = user.nickName
            tow['avatarUrl'] = user.avatarUrl
            tow['gender'] = user.gender
            obj['user'] = tow

            list_data.append(obj)

        data = {'status': 1,
                'index_news': list_data
                }
        return JsonResponse(data)
    else:
        data = {'status': 0,
                'index_news': list_data
                }
        return JsonResponse(data)



#我的发帖
def show_mytiezi(request):
    userid = request.GET.get('userid')
    tiezis = News.objects.filter(userid = userid,isdelete = 0).order_by('-id')
    list_data = []
    for news in tiezis:
        obj = {}
        one = to_dict(news)
        one['tiezi_id'] = one.pop('id')
        one['time'] = str(one['time'])[:19].replace('T', ' ')
        one.pop('only_title')
        list_data.append(one)
    data = {'status': 1,
            'mytiezi': list_data
            }
    return JsonResponse(data)


##我的精华帖
def show_myessence(request):
    userid = request.GET.get('userid')
    tiezis = News.objects.filter(Q(userid = userid)&Q(good_num__gt=199)&Q(isdelete = 0))
    list_data = []
    for news in tiezis:
        obj = {}
        one = to_dict(news)
        one['tiezi_id'] = one.pop('id')
        one['time'] = str(one['time'])[:19].replace('T', ' ')
        one.pop('only_title')
        list_data.append(one)
    data = {'status': 1,
            'mytiezi': list_data
            }
    return JsonResponse(data)


#我的未读消息
def show_mynews(request):
    userid = request.GET.get('userid')
    result_data = {}
    news_list = []

    #点赞了你的帖子
    good_fortiezis = Good_num_tiezi.objects.filter(Q(get_good_man=userid) & Q(isread=0)&Q(isdelete=0)).exclude(make_good_man =userid)

    if good_fortiezis.exists():
        for good_fortiezi in good_fortiezis:
            tiezi_id = good_fortiezi.tiezi_id


            # if tiezi_id not in good_for_tiezis:
            make_good_man = good_fortiezi.make_good_man
            user = User.objects.get(userid=make_good_man)
            username = user.nickName
            avatarUrl= user.avatarUrl
            user_obj = {'username':username,'avatarUrl':avatarUrl,'good_num_tiezi_id':good_fortiezi.id,'good_num_maincomment_id':'',
                        'tiezi_id':tiezi_id,'tablename':'Good_num_tiezi','main_comment_id':'','side_comment_id':'','type':1}
            news_list.append(user_obj)


    # 点赞了你的评论
    good_formiancomments = Good_num_maincomment.objects.filter(Q(get_good_man=userid) & Q(isread=0)&Q(isdelete=0)).exclude(make_good_man =userid)
    if good_formiancomments.exists():
        for good_formiancomment in good_formiancomments:
            main_comment_id = good_formiancomment.main_comment_id
            #if main_comment_id not in good_for_comments:
            make_good_man = good_formiancomment.make_good_man
            user = User.objects.get(userid=make_good_man)
            username = user.nickName
            avatarUrl = user.avatarUrl

            tiezi_id = Main_comment.objects.get(pk = main_comment_id).tiezi_id
            user_obj = {'username': username, 'avatarUrl': avatarUrl, 'ismany': 0,'tiezi_id':tiezi_id,'good_num_tiezi_id':'','good_num_maincomment_id':good_formiancomment.id,
                        'tablename':'Good_num_maincomment','main_comment_id':main_comment_id,'side_comment_id':'','type':2}
            news_list.append(user_obj)

    #评论了你的帖子
    main_comments = Main_comment.objects.filter(Q(to_man=userid) & Q(main_isread=0)).exclude(main_openor =userid)
    if main_comments.exists():
        for main_comment in main_comments:
            tiezi_id = main_comment.tiezi_id
            #if tiezi_id not in comment_for_tiezis:
            make_comment_man  = main_comment.main_openor
            user = User.objects.get(userid=make_comment_man)
            username = user.nickName
            avatarUrl = user.avatarUrl
            content = main_comment.com_content
            user_obj = {'username': username, 'avatarUrl': avatarUrl, 'ismany': 0,'content':content,'good_num_tiezi_id':'','good_num_maincomment_id':'',
                        'tiezi_id':tiezi_id,'tablename':'Main_comment','main_comment_id':main_comment.id,'side_comment_id':'','type':3,}
            news_list.append(user_obj)


    #回复了你的评论
    side_comments = Side_comment.objects.filter(Q(to_man=userid) & Q(side_isread=0)).exclude(side_openor =userid)
    if side_comments.exists():
        for side_comment in side_comments:
            main_comment_id = side_comment.main_comment_id
            #if main_comment_id not in back_your_comment:

            make_comment_man = side_comment.side_openor
            user = User.objects.get(userid=make_comment_man)
            username = user.nickName
            avatarUrl = user.avatarUrl
            content = side_comment.side_com_content
            tiezi_id = side_comment.tiezi_id
            user_obj = {'username': username, 'avatarUrl': avatarUrl, 'ismany': 0, 'content': content,'good_num_tiezi_id':'','good_num_maincomment_id':'',
                        'tiezi_id': tiezi_id,'tablename':'Side_comment','main_comment_id':main_comment_id,'type':4,'side_comment_id':side_comment.id}
            news_list.append(user_obj)
    result_data['news_list'] = news_list

    return JsonResponse(result_data)



#阅读此条消息
def read_show_detail(request):
    tiezi_id = int(request.POST.get('tiezi_id'))
    userid = request.POST.get('userid')
    tablename = request.POST.get('tablename')
    main_comment_id =request.POST.get('main_comment_id')
    side_comment_id = request.POST.get('side_comment_id')
    good_num_tiezi_id = request.POST.get('good_num_tiezi_id')
    good_num_maincomment_id = request.POST.get('good_num_maincomment_id')
    #修改数据库
    #'good_num_tiezi_id': good_fortiezi.id, 'good_num_maincomment_id': '',
    if tablename == 'Good_num_tiezi':
        data = Good_num_tiezi.objects.get(pk = good_num_tiezi_id)
        data.isread = 1
        data.save()
    elif tablename == 'Good_num_maincomment':
        data = Good_num_maincomment.objects.get(pk = good_num_maincomment_id)
        data.isread = 1
        data.save()
    elif tablename == 'Main_comment':
        data = Main_comment.objects.get(pk = main_comment_id)
        data.main_isread = 1
        data.save()
    else :
        data = Side_comment.objects.get(pk = side_comment_id)
        data.side_isread = 1
        data.save()

    #展示帖子详情
    obj = {}
    news = News.objects.get(id=tiezi_id)
    tiezi_data = {}
    tiezi_data['tiezi_id'] = news.id
    user=news.userid
    tiezi_data['userid'] = user
    tiezi_data['title'] = news.title
    tiezi_data['img1'] = news.img1
    tiezi_data['img2'] = news.img2
    tiezi_data['img3'] = news.img3
    tiezi_data['time'] = str(news.time)[:19].replace('T',' ')
    tiezi_data['content'] = news.content

    # 判断当前用户是否点赞主贴
    isgood_forTiezi = Good_num_tiezi.objects.filter(Q(tiezi_id=tiezi_id) & Q(make_good_man=userid))
    if isgood_forTiezi.exists():
        tiezi_data['isgood_forTiezi'] = 1
    else:
        tiezi_data['isgood_forTiezi'] = 0

    #判断是否收藏该帖子
    iscollect_forTiezi = Collect_tiezi.objects.filter(Q(tiezi_id=tiezi_id) & Q(collector=userid))
    if iscollect_forTiezi.exists():
        tiezi_data['iscollect_forTiezi'] = 1
    else:
        tiezi_data['iscollect_forTiezi'] = 0


    writor = User.objects.get(openId=user[:-3])
    tiezi_data['writor_nikename'] = writor.nickName
    tiezi_data['writor_avatarUrl'] = writor.avatarUrl


    maincomments = Main_comment.objects.filter(tiezi_id=tiezi_id).order_by('id')
    main_list = []
    for maincomment in maincomments:
        main_data = {}
        mian_id = maincomment.id
        main_data['id'] =mian_id
        main_data['com_content'] = maincomment.com_content
        main_data['good_num'] = maincomment.good_num
        main_data['tiezi_id'] = maincomment.tiezi_id

        main_user=maincomment.main_openor
        main_data['main_openor'] = main_user
        Mainuser = User.objects.get(openId=main_user[:-3])
        main_data['from_main_nickname']= Mainuser.nickName
        main_data['from_main_avatarurl'] = Mainuser.avatarUrl



        sidecomments = Side_comment.objects.filter(main_comment_id=mian_id).order_by('id')
        side_list = []
        for sidecomment in sidecomments:
            side_data = {}
            side_data['main_comment_id'] = sidecomment.main_comment_id
            side_data['id'] = sidecomment.id
            side_data['tiezi_id'] = sidecomment.tiezi_id
            side_data['side_com_content'] = sidecomment.side_com_content

            sideopenor = sidecomment.side_openor
            side_data['side_openor'] = sideopenor
            Sideopenor = User.objects.get(openId=sideopenor[:-3])
            side_data['from_side_nickname'] = Sideopenor.nickName
            sidecommentz_to_man =sidecomment.to_man
            side_data['sidecomment_to_man'] = sidecommentz_to_man
            Sidecommentz_to_man = User.objects.get(openId=sidecommentz_to_man[:-3])
            side_data['to_side_nickname'] = Sidecommentz_to_man.nickName

            side_list.append(side_data)

        main_data['sidecomments']=side_list
        main_list.append(main_data)

    tiezi_data['maincomments']= main_list
    obj['tiezi_data'] = tiezi_data

    return  JsonResponse({'status': 1, 'data': obj})


def delete_news(request):
    tiezi_id = int(request.GET.get('tieziid'))
    news = News.objects.get(id = tiezi_id)
    news.isdelete = 1
    news.save()
    userid = news.userid
    user = User.objects.get(userid = userid)
    user.post_num -= 1
    user.experience -= 10
    user.save()
    Good_num_tiezi.objects.filter(tiezi_id = tiezi_id).update(isread=1)

    main_comment = Main_comment.objects.filter(tiezi_id = tiezi_id)
    if main_comment.exists():
        for themain in main_comment:
            themain.main_isread = 1
            themain.save()
            Good_num_maincomment.objects.filter(main_comment_id=themain.id).update(isread=1)
            Side_comment.objects.filter(main_comment_id=themain.id).update(side_isread=1)
    return JsonResponse({'status':1})