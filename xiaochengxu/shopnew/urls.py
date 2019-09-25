
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^zhoubian_goods/$', views.zhoubian_goods),
    url(r'^thezhoubian/$', views.thezhoubian),
    url(r'^getcale/$', views.getcale),
    url(r'^getlocation_note/$', views.getlocation_note),
    url(r'^record_location/$', views.record_location),
    url(r'^del_location/$', views.del_location),
    url(r'^change_location/$', views.change_location),
    url(r'^getdefault_location/$', views.getdefault_location),
    url(r'^makeorder/$', views.makeorder),
    url(r'^query_pay/$', views.query_pay_state),
    url(r'^addtocar/$', views.addtocar),
    url(r'^showcar/$', views.showcar),
    url(r'^deltocar/$', views.deltocar),
    url(r'^getnumforcar/$', views.getnumforcar),
    url(r'^zhoubianorder/$', views.myorder),
    url(r'^cancelorder/$', views.cancelorder),
    url(r'^deleteorder/$', views.deleteorder),
    url(r'^makesure_get/$', views.makesure_get),
    url(r'^showtheorder/$', views.showtheorder),
    url(r'^repay/$', views.repay),
]
