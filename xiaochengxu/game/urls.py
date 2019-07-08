
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^fly/$', views.fly),
    url(r'^putscore/$', views.putscore),
]
