
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^allactivety/$', views.allactivety),
    url(r'^theactivety/$', views.theactivety),
    url(r'^join/$', views.join),
    url(r'^isjoin/$', views.isjoin),
    url(r'^myjoin/$', views.myjoin),
    url(r'^myprize/$', views.myprize),
    url(r'^mycoupon/$', views.mycoupon),
    url(r'^getcoupon/$', views.getcoupon),
]
