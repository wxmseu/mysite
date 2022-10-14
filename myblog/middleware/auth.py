from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    """中间件1"""

    def process_request(self, request):
        # 0.排除那些不需要登录就可以访问的页面
        # request.path_info获取当前用户请求的url
        url_no_need_login = ['/login/', '/', '/image/code/', '/register/', '/register/confirm/']
        url_present = request.path_info
        if url_present in url_no_need_login:
            return
        # 1.读取访问当前用户的session信息，如果能读取到说明已登录过
        info = request.session.get('info')
        if info:
            return
        # 2. 如果没有登录过，就返回登录页面
        else:
            return redirect('/login')
