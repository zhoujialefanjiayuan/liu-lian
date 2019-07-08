
from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^show_all/$', views.show_all),
    url(r'^show_swiper/$', views.show_swiper),
    url(r'^search/$', views.search),
    url(r'^getpicture/$', views.getpicture),
    url(r'^addvisit/$', views.addvisit),
    url(r'^qiniuyun_uptoken/$', views.qiniuyun_uptoken),
]
