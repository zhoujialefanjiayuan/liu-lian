
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^not_send/$', views.not_send),
    url(r'^login/$', views.login),
    url(r'^getorder/$', views.getorder),
    url(r'^needsend/$', views.needsend),
    url(r'^orderdetail/$', views.orderdetail),
    url(r'^issended/$', views.issended),
]
