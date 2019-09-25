import datetime

from django.db import models

# Create your models here.
#发布帖子
t = datetime.datetime.strptime('2019-06-28','%Y-%m-%d')
class News(models.Model):
    userid = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    only_title = models.CharField(max_length=100,default=0,db_index=True)
    content = models.TextField(max_length=1024)
    time = models.DateTimeField(auto_now_add=True)
    img1 =  models.CharField(max_length=200,default='nopicture')
    img2 = models.CharField(max_length=200, default='nopicture')
    img3 = models.CharField(max_length=200, default='nopicture')
    top = models.BooleanField(default=0)
    comment_num = models.IntegerField(default=0)
    good_num = models.IntegerField(default=0)
    isswiper = models.BooleanField(default=0)
    isdelete = models.BooleanField(default=0)


#主评论表
class Main_comment(models.Model):
    tiezi_id = models.IntegerField()
    main_openor = models.CharField(max_length=50) #openId
    com_content =  models.CharField(max_length=200)
    good_num = models.IntegerField(default=0)
    to_man =  models.CharField(max_length=50) #发表帖子的人openId
    main_isread = models.BooleanField(default=0)
    opentime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now_add=True)
#副评论表
class Side_comment(models.Model):
    main_comment_id = models.IntegerField()
    side_openor = models.CharField(max_length=50) #openId
    side_com_content =  models.CharField(max_length=200)
    tiezi_id = models.IntegerField(default=0)
    to_man = models.CharField(max_length=50)  # 发表主评论的人openId
    side_isread = models.BooleanField(default=0)
    opentime = models.DateTimeField(auto_now_add=True)




#点赞帖子表
class Good_num_tiezi(models.Model):
    #点赞人
    make_good_man = models.CharField(max_length=50)
    #被点赞人
    get_good_man = models.CharField(max_length=50)
    #帖子id
    tiezi_id = models.IntegerField()
    isread = models.BooleanField(default=0)
    isdelete = models.BooleanField(default=0)


#点赞主评论表
class Good_num_maincomment(models.Model):
    #点赞人
    make_good_man = models.CharField(max_length=50)
    # 被点赞人
    get_good_man = models.CharField(max_length=50)
    #主评论表id
    main_comment_id = models.IntegerField()
    isread = models.BooleanField(default=0)
    isdelete = models.BooleanField(default=0)

#收藏帖子
class Collect_tiezi(models.Model):
    collector = models.CharField(max_length=50)
    tiezi_id= models.CharField(max_length=10)


#记录举报内容
class Report(models.Model):
    tiezi_id = models.IntegerField()
    content = models.CharField(max_length=255)