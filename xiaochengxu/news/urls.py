
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^write_news/$', views.write_news),  # 写帖子
    url(r'^delete_news/$', views.delete_news),  # 写帖子
    url(r'^show_indexnews/$', views.indexshow_news),  # 首页展示帖子
    url(r'^topnews/$', views.topnews),  # 榜单帖子
    url(r'^focouse_news/$', views.focousenews),  # 关注帖子
    url(r'^recomend_news/$', views.recomend_news),  # 推荐帖子
    url(r'^search_news/$', views.search), #搜索帖子
    url(r'^swipper_news/$', views.swipper), #轮播图帖子
    url(r'^choiceness_news/$', views.choiceness_news),
    url(r'^main_comment/$', views.main_comment),
    url(r'^side_comment/$', views.side_comment),
    url(r'^show_detail/$', views.show_detail),
    url(r'^onepage/$', views.onepage),
    url(r'^topcomments/$', views.topcomments),
    url(r'^good_fortiezi/$', views.good_fortiezi),
    url(r'^delgood_fortiezi/$', views.delgood_fortiezi),
    url(r'^good_formiancomment/$', views.good_formiancomment),
    url(r'^delgood_formiancomment/$', views.delgood_formiancomment),
    url(r'^collect_tiezi/$', views.collect),
    url(r'^delcollect_tiezi/$', views.delcollect),
    url(r'^report/$', views.report),
    url(r'^show_mycollect/$', views.show_mycollect),
    url(r'^show_mygood/$', views.show_mygood),
    url(r'^show_mycomment/$', views.show_mycomment),
    url(r'^show_mytiezi/$', views.show_mytiezi),
    url(r'^show_myessence/$', views.show_myessence),
    url(r'^show_mynews/$', views.show_mynews),
    url(r'^read_show_detail/$', views.read_show_detail),
]
