from django.db import models

# Create your models here.
class Vocal(models.Model):
    project_name = models.CharField(max_length=50)
    little_img = models.CharField(max_length=100,default=1)
    singger = models.CharField(max_length=60)
    city = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    time =  models.CharField(max_length=50)
    picture_num = models.IntegerField(default=0)
    visit_num = models.IntegerField(default=0)
    isswiper = models.BooleanField(default=0)


class Picture(models.Model):
    project_id = models.IntegerField()
    picture_small = models.CharField(max_length=512)
    picture_big = models.CharField(max_length=512)
    look_num = models.IntegerField(default=0)




