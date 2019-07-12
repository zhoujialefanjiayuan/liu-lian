import time

from django.core import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from xiaochengxu import settings


class CountipMiddle(MiddlewareMixin):
    # 在视图执行前调用
    def process_request(self,request):
        # 获取客户端ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip(若经过负载均衡，和代理有此项)
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        black_ips = getattr(settings, 'BLOCKED_IPS')
        if ip in black_ips:
            return HttpResponse('404')
        loadtime = cache.cache.get(ip)
        if loadtime:
            now = time.time()
            cache.cache.set(ip,now)
            if now-loadtime < 0.5:
                black_ips.append(ip)
                setattr(settings, 'BLOCKED_IPS', black_ips)
                return HttpResponse('404')
        else:
            cache.cache.set(ip, 1, 10)
