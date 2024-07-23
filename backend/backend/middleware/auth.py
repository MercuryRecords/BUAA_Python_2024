from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class Authentication(MiddlewareMixin):
    def process_request(self, request):
        if request.method != "POST":
            return JsonResponse({"code": 400, "message": "请求方式错误"})
        
        if request.path_info in ['/api/user_register/', '/api/user_login/']:
            return
        
        register_name = request.session.get("username")
        user_name = request.POST.get("username")

        # print(request.path_info, register_name, user_name)
        if not register_name or register_name != user_name:
            # 注掉 return 可禁用用户认证
            return JsonResponse({"code": 400, "message": "请先登录"})
        