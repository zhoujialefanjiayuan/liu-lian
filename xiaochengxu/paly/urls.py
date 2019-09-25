
from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^1/$', views.helloword),#测试
    url(r'^getid/$', views.getid),#测试连接开发服务器
    url(r'^getuser/$', views.getuser),
    url(r'^gomine/$', views.go_mine),
    url(r'^notreadnews/$', views.notreadnews),
    url(r'^getuserdata/$', views.browseuserdata),#浏览用户详情
    url(r'^concern/$', views.concern),
    url(r'^no_concern/$', views.no_concern),
    url(r'^myconcern/$', views.myconcern),
    url(r'^myfans/$', views.myfans),
]
