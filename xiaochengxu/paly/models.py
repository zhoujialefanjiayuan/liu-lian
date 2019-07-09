from django.db import models

# Create your models here.
# 参考数据
# {'openId': 'o3S7I5VDKwKP2005blNM92uRwaQk', 'nickName': '乐～', 'gender': 1,
# 'language': 'zh_CN', 'city': 'Yueyang', 'province': 'Hunan', 'country': 'China',
# 'avatarUrl': 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKABUOialWDJn5O8LzCXjySvRF7xnTE6Xv4czhKUyT1Qb04QAzic3amCfZGoBwCafepvFZ7YmcXCpeQ/132',
#  'unionId': 'o2o3m1HOuzMP5yEX0X2uxBzNPWC0', 'watermark': {'timestamp': 1554208372, 'appid': 'wxc50f63e5b68a91f4'}}
# """
class User(models.Model):
    userid  = models.CharField(max_length=50,default='nothing')
    openId = models.CharField(max_length=50,primary_key=True)
    nickName = models.CharField(max_length=30)
    gender = models.IntegerField(default=1)
    language = models.CharField(max_length=10,default='none')
    city = models.CharField(max_length=10,default='none')
    province = models.CharField(max_length=10,default='none')
    country = models.CharField(max_length=10,default='none')
    avatarUrl = models.CharField(max_length=256,default='none')
    unionId = models.CharField(max_length=30)
    token = models.CharField(max_length=100,default='nothing',unique=True)
    experience = models.IntegerField(default=0)
    post_num = models.IntegerField(default=0) #发帖数
    concern_num = models.IntegerField(default=0)
    fans_num = models.IntegerField(default=0)

class Concern(models.Model):
    userid = models.CharField(max_length=50)
    concern_userid = models.CharField(max_length=50)
    concern = models.ForeignKey(User)


class Fans(models.Model):
    userid = models.CharField(max_length=50)
    fans_userid = models.CharField(max_length=50)
    fans = models.ForeignKey(User)
