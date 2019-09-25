from django.db import models

# Create your models here.

class Userforsendor(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    token = models.CharField(max_length=100)

