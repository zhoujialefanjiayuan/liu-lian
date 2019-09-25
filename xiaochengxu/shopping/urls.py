
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^goods_type/$', views.goods_type),
    url(r'^goods/$', views.newgoods),
    url(r'^showzhoubian/$', views.showzhoubian),
    url(r'^thezhoubian/$', views.thezhoubian),
    url(r'^post_zhoubianorder/$', views.post_zhoubianorder),#提交周边订单
    url(r'^get_wxnotice_pay/$', views.get_wxnotice_pay),#支付通知
    url(r'^query_pay_state/$', views.query_pay_state),#查询支付状态
    url(r'^get_wxnotice_refund/$', views.get_wxnotice_refund),#退款通知
    url(r'^ready_pay/$', views.ready_pay),#待支付状态下的再次支付
    url(r'^refundment/$', views.refundment),#退款
    url(r'^myorder/$', views.myorder),
    url(r'^closeorder/$', views.closeorder),
    url(r'^return_goods/$', views.return_goods),
    url(r'^cancel_return/$', views.cancel_return),
    url(r'^refuse_return/$', views.refuse_return),
    url(r'^post_xianchangorder/$', views.post_xianchangorder),
    url(r'^qureypay_forxianchang/$', views.qureypay_forxianchang),
    url(r'^showorder_forxianchang/$', views.showorder_forxianchang),
    url(r'^loactionforxianchang/$', views.loactionforxianchang),
]
