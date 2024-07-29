from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class Authentication(MiddlewareMixin):
    def process_request(self, request):
        # print(request.POST)
        if request.method == "GET" and request.path_info.startswith(r"/media/avatars/"):
            return
        # return
        if request.method != "POST":
            return JsonResponse({"code": 400, "message": "请求方式错误"})

        if request.path_info in ['/api/user_register', '/api/user_login', '/api/user_register/', '/api/user_login/']:
            return
        # 加 return 禁用用户认证
        # return

        register_name = request.session.get("username")
        user_name = request.POST.get("username")

        # print(request.path_info, register_name, user_name)
        if not register_name or register_name != user_name:
            return JsonResponse({"code": 400, "message": "请先登录"})

        is_admin = request.session.get("usertype") == '0'
        is_admin_path = request.path_info.startswith('/api/admin_')

        if is_admin_path and not is_admin:
            return JsonResponse({"code": 400, "message": "普通用户无权限访问管理员接口"})

        if not is_admin_path and is_admin:
            return JsonResponse({"code": 400, "message": "管理员用户不应访问普通用户接口"})
