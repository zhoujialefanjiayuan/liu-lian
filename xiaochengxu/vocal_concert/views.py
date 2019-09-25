from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page

from vocal_concert.models import *
from qiniu import Auth

def qiniu_token(key):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'gBkv_k7il3Q-EakwjqXS9v5Dv4U8NTB_rEL2hftD'
    secret_key = 'WX41hT6RDqD2qB04BY364aNBcprexLPIdFUUdqmC'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'xiaochengxu'

    # 上传到七牛后保存的文件名
    key = key
    # 生成上传 Token，可以指定过期时间等

    # 上传策略示例
    # https://developer.qiniu.com/kodo/manual/1206/put-policy
    # policy = {
    #     # 'callbackUrl':'https://requestb.in/1c7q2d31',
    #     # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
    #     # 'persistentOps':'imageView2/1/w/200/h/200'
    # }

    token = q.upload_token(bucket_name, key, 3600)

    return token

def to_dict(obj):
    '''将当前对象转换成字典'''
    attr_dict = {}
    for field in obj._meta.get_fields():
        name = field.attname  # 属性名
        value = getattr(obj, name)  # 属性值
        attr_dict[name] = value
    return attr_dict


def show_all(request):
    vocals=Vocal.objects.order_by('-id')
    singger_img = Singger_img.objects.all()
    singger_list = []
    for i in singger_img:
        obj = {}
        obj['siggger_img'] = i.siggger_img
        obj['siggger_name'] =i.siggger_name
        singger_list.append(obj)
    if len(vocals) > 6:
        vocals= vocals[:6]
        ismore = True
    else:
        ismore = False
    list_data = []
    for vocal in vocals:
        obj = {}
        sing = vocal.singger
        ci = vocal.city
        obj['id'] = vocal.id
        obj['project_name'] = vocal.project_name
        obj['little_img'] = vocal.little_img
        obj['singger'] = sing
        obj['city'] = ci
        obj['location'] = vocal.location
        obj['time'] = vocal.time
        obj['picture_num'] = vocal.picture_num
        obj['visit_num'] = vocal.visit_num
        list_data.append(obj)
    return JsonResponse({'status':1,'data':list_data,'ismore':ismore,'singger_list':singger_list})



@cache_page(600)
def show_swiper(request):
    vocals = Vocal.objects.filter(isswiper = 1)
    list_data = []
    for vocal in vocals:
        obj = {}
        obj['id'] = vocal.id
        obj['project_name'] = vocal.project_name
        obj['little_img'] = vocal.little_img
        obj['singger'] = vocal.singger
        obj['city'] = vocal.city
        obj['location'] = vocal.location
        obj['time'] = vocal.time
        obj['picture_num'] = vocal.picture_num
        obj['visit_num'] = vocal.visit_num
        list_data.append(obj)
    return JsonResponse({'status': 1, 'data': list_data})


def search(request):
    singger = request.GET.get('singger').strip()
    if singger !='全部':
        vocals = Vocal.objects.filter(singger__contains=singger)
    else:
        vocals = Vocal.objects.all()
    list_data = []
    for vocal in vocals:
        obj = {}
        obj['id'] = vocal.id
        obj['project_name'] = vocal.project_name
        obj['little_img'] = vocal.little_img
        obj['singger'] = vocal.singger
        obj['city'] = vocal.city
        obj['location'] = vocal.location
        obj['time'] = vocal.time
        obj['picture_num'] = vocal.picture_num
        obj['visit_num'] = vocal.visit_num
        list_data.append(obj)
    return JsonResponse({'status': 1, 'list_data': list_data})

# def get_detail(request):
#     id = request.GET.get('id')
#     try:
#         vocal= Vocal.objects.get(pk=id)
#         vocal = to_dict(vocal)
#         return JsonResponse({'status': 1, 'data': vocal})
#     except:
#         return JsonResponse({'status': 0, 'data': 'id is error or none'})



def qiniuyun_uptoken(request):
    filename = request.GET.get('filename')
    print(filename)
    uptoken = qiniu_token(filename)
    return JsonResponse({'status':1,'uptoken':uptoken,'expire':3600,'domain':'xcx.szbeacon.com'})


@cache_page(10)
def getpicture(request):
    projectid = int(request.GET.get('projectid'))
    pictures = Picture.objects.filter(project_id = projectid)
    orderpic = pictures.order_by('look_num')[:10]
    picturelist = []
    hotpicturelist = []
    for picture in pictures:
        p = to_dict(picture)
        picturelist.append(p)
    for o in orderpic:
        o = to_dict(o)
        hotpicturelist.append(o)
    return JsonResponse({'picturelist':picturelist,'hotpicturelist':hotpicturelist})

#访问量统计
def addvisit(request):
    projectid = int(request.GET.get('projectid'))
    pictureid = int(request.GET.get('pictureid'))
    picture = Picture.objects.get(id=pictureid)
    project = Vocal.objects.get(id=projectid)
    picture.look_num +=1
    project.visit_num +=1
    picture.save()
    project.save()
    return JsonResponse({'status':1})

def thevoacl(request):
    projectid = int(request.GET.get('projectid'))
    vocal = Vocal.objects.get(pk = projectid)
    obj = {}
    obj['id'] = vocal.id
    obj['project_name'] = vocal.project_name
    obj['little_img'] = vocal.little_img
    obj['singger'] = vocal.singger
    obj['city'] = vocal.city
    obj['location'] = vocal.location
    obj['time'] = vocal.time
    obj['picture_num'] = vocal.picture_num
    obj['visit_num'] = vocal.visit_num
    return JsonResponse({'status':1,'data':obj})

def singgerimg(request):
    vocals=Vocal.objects.order_by('-visit_num')





