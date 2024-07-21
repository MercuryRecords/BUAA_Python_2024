from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from .models import User, Manager, Group, JoinRequest


@require_http_methods(["POST"])
def message(request):
    mes = request.POST.get('message')
    return HttpResponse(mes[0])


@require_http_methods(["POST"])
def user_register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    usertype = request.POST.get('usertype')
    check = True
    if usertype == '0':
        # 创建管理员用户
        check = Manager.objects.filter(username=username)
    elif usertype == '1':
        check = User.objects.filter(username=username)
    print(f"usertype: {usertype}, username: {username}, password: {password}, check: {check}")
    if check:
        # 用户名已经存在，不予注册，返回错误信息
        res = {"code": 401, "message": "用户名已存在"}
        return JsonResponse(res)
    else:
        if username == "" or len(username) > 100:
            res = {"code": 402, "message": "用户名不能为空且长度不能超过100"}
            return JsonResponse(res)

        if password == "" or len(password) > 100:
            res = {"code": 403, "message": "密码不能为空且长度不能超过100"}
            return JsonResponse(res)

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


@require_http_methods(["POST"])
def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    usertype = request.POST.get('usertype')

    check = None
    if usertype == '0':
        # 创建管理员用户
        check = Manager.objects.filter(username=username)
    elif usertype == '1':
        check = User.objects.filter(username=username)

    if check is None:
        return JsonResponse({"code": 401, "message": "用户名不存在"})

    # 检查密码是否正确
    if check[0].password != password:
        return JsonResponse({"code": 402, "message": "密码错误"})

    return JsonResponse({"code": 200, "message": "登录成功"})


@require_http_methods(["POST"])
def group_create(request):
    username = request.POST.get('username')
    group_name = request.POST.get('group_name')
    group_description = request.POST.get('group_description')

    # 检查用户是否存在
    check = User.objects.filter(username=username)

    if not check:
        return JsonResponse({"code": 401, "message": "用户不存在"})

    if len(group_name) > 100:
        return JsonResponse({"code": 402, "message": "群组名长度不能超过100"})

    # 检查群组名是否已经存在
    if Group.objects.filter(group_name=group_name).exists():
        return JsonResponse({"code": 403, "message": "群组名已存在"})

    if len(group_description) > 200:
        return JsonResponse({"code": 404, "message": "群组描述长度不能超过200"})

    # 创建群组
    Group.objects.create(name=group_name, description=group_description, created_by=check[0])
    return JsonResponse({"code": 200, "message": "群组创建成功"})


@require_http_methods(["POST"])
def group_apply_to_join(request):
    username = request.POST.get('username')
    group_name = request.POST.get('group_name')
    apply_reason = request.POST.get('apply_reason')

    # 检查用户是否存在
    check = User.objects.filter(username=username)

    if not check:
        return JsonResponse({"code": 401, "message": "用户不存在"})

    # 检查群组是否存在
    group = Group.objects.filter(group_name=group_name)

    if not group:
        return JsonResponse({"code": 402, "message": "群组不存在"})

    # 检查用户是否已经申请过该群组
    if JoinRequest.objects.filter(user=check[0], group=group[0]).exists():
        return JsonResponse({"code": 403, "message": "用户正在申请加入该群组"})

    # 检查申请理由长度是否超过200
    if len(apply_reason) > 200:
        return JsonResponse({"code": 404, "message": "申请理由长度不能超过200"})

    # 创建申请
    JoinRequest.objects.create(user=check[0], group=group[0], apply_reason=apply_reason)
    return JsonResponse({"code": 200, "message": "申请已提交"})


@require_http_methods(["POST"])
# 根据审核意见处理申请
def group_handle_join_request(request):
    applier_name = request.POST.get('applier_name')
    group_name = request.POST.get('group_name')
    owner_name = request.POST.get('owner_name')
    approval = request.POST.get('approval')
    # 检查用户是否存在
    check = User.objects.filter(username=applier_name)
    if not check:
        return JsonResponse({"code": 401, "message": "用户不存在"})

    # 检查群组是否存在
    group = Group.objects.filter(group_name=group_name)
    if not group:
        return JsonResponse({"code": 402, "message": "群组不存在"})

    # 检查群主是否为该群组的创建者
    if group[0].created_by.username != owner_name:
        return JsonResponse({"code": 403, "message": "群主不是该群组的创建者"})

    # 根据 approval的值来决定是否同意申请
    JoinRequest.objects.filter(user=check[0], group=group[0]).delete()
    if approval == '1':
        # 同意申请
        group[0].members.add(check[0])
        return JsonResponse({"code": 200, "message": "申请已同意"})
    else:
        # 拒绝申请
        return JsonResponse({"code": 200, "message": "申请已拒绝"})
