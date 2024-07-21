from django.http import JsonResponse, HttpResponse

from .models import User, Manager


def message(request):
    mes = request.POST.get('message')
    return HttpResponse(mes[0])


# Create your views here.
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usertype = request.POST.get('usertype')
        check = True
        if usertype == '0':
            # 创建管理员用户
            check = Manager.objects.filter(username=username)
        elif usertype == '1':
            check = User.objects.filter(username=username)
        if check:
            # 用户名已经存在，不予注册，返回错误信息
            res = {"code": 401, "message": "用户名已存在"}
            return JsonResponse(res)
        else:
            # 创建用户并加入到数据库中，返回注册成功信息
            if usertype == '0':
                # 创建管理员用户
                Manager.objects.create(username=username, password=password)
                res = {"code": 200, "message": "管理员注册成功"}
                return JsonResponse(res)
            elif usertype == '1':
                User.objects.create(username=username, password=password)
                res = {"code": 200, "message": "用户注册成功"}
                return JsonResponse(res)

    else:
        # 不是 POST 请求
        return JsonResponse({"code": 400, "message": "请求方式错误"})
