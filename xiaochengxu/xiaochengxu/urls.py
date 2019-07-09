"""xiaochengxu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from paly import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello/',views.helloword ),
    url(r'^user/',include('paly.urls',namespace='user')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^vocal/', include('vocal_concert.urls', namespace='vocal_concert')),
    url(r'^shop/', include('shopping.urls', namespace='shop')),
    url(r'^activety/', include('activety.urls', namespace='activety'))
]
