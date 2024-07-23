from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import User, Group, ProblemGroup


@require_http_methods(["POST"])
def admin_register_user(request):
    # 注册新用户
    username = request.POST.get('name')
    password = request.POST.get('password')
    check = User.objects.filter(username=username)
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

        user = User.objects.create(username=username, password=password)
        ProblemGroup.objects.create(user=user, title="默认分组")
        res = {"code": 200, "message": "用户注册成功"}
        return JsonResponse(res)


@require_http_methods(["POST"])
def admin_manage_user_profile(request):
    # 修改个人信息，虽然现在还不知道有什么个人信息
    pass


@require_http_methods(["POST"])
def admin_delete_user(request):
    # 删除用户
    username = request.POST.get('name')
    check = User.objects.filter(username=username)
    if not check:
        # 用户不存在，返回错误信息
        res = {"code": 401, "message": "用户不存在"}
        return JsonResponse(res)

    check.delete()
    res = {"code": 200, "message": "用户删除成功"}
    return JsonResponse(res)


@require_http_methods(["POST"])
def admin_delete_group(request):
    # 删除用户组
    group_name = request.POST.get('group_name')
    check = Group.objects.filter(name=group_name)

    if not check:
        # 用户组不存在，返回错误信息
        res = {"code": 401, "message": "用户组不存在"}
        return JsonResponse(res)

    check.delete()
    res = {"code": 200, "message": "用户组删除成功"}
    return JsonResponse(res)


@require_http_methods(["POST"])
def admin_add_user_to_group(request):
    # 使用户加入用户组
    username = request.POST.get('name')
    group_name = request.POST.get('group_name')
    check = User.objects.filter(username=username)
    check2 = Group.objects.filter(name=group_name)
    if not check or not check2:
        # 用户或用户组不存在，返回错误信息
        res = {"code": 401, "message": "用户或用户组不存在"}
        return JsonResponse(res)

    check2[0].members.add(check[0])
    res = {"code": 200, "message": "用户加入用户组成功"}
    return JsonResponse(res)


@require_http_methods(["POST"])
def admin_remove_user_from_group(request):
    # 使用户退出用户组
    username = request.POST.get('name')
    group_name = request.POST.get('group_name')
    check = User.objects.filter(username=username)
    check2 = Group.objects.filter(name=group_name)
    if not check or not check2:
        # 用户或用户组不存在，返回错误信息
        res = {"code": 401, "message": "用户或用户组不存在"}
        return JsonResponse(res)

    check2[0].members.remove(check[0])
    res = {"code": 200, "message": "用户退出用户组成功"}
    return JsonResponse(res)


@require_http_methods(["POST"])
def admin_edit_group_info(request):
    # 修改用户组信息
    group_name = request.POST.get('group_name')
    new_description = request.POST.get('new_description')

    check = Group.objects.filter(name=group_name)

    if not check:
        # 用户组不存在，返回错误信息
        res = {"code": 401, "message": "用户组不存在"}
        return JsonResponse(res)

    check.update(description=new_description)
    res = {"code": 200, "message": "用户组信息修改成功"}
    return JsonResponse(res)


@require_http_methods(["POST"])
# 管理员获得第 i 页的用户名单
def admin_get_user_list(request):
    page = int(request.POST.get('page')) - 1
    users = User.objects.all()
    # 每10个用户一页，按照用户名排序；先检查是否越界
    # 越界检查

    if page * 10 >= users.count():
        res = {"code": 401, "message": "用户列表获取失败，页码越界"}
        return JsonResponse(res)

    if (page + 1) * 10 > users.count():
        users = users.order_by('username')[10 * page:]
    else:
        users = users.order_by('username')[10 * page:10 * (page + 1)]

    # 返回用户相关信息

    res = {"code": 200, "message": "用户列表获取成功", "data": [{"username": user.username, "password": user.password, "groups": [group.name for group in user.groups.all()]} for user in users]}
    return JsonResponse(res)


@require_http_methods(["POST"])
# 管理员获得第 i 页的用户组名单
def admin_get_group_list(request):
    page = int(request.POST.get('page')) - 1
    groups = Group.objects.all()
    # 每10个用户组一页，按照用户组名排序；先检查是否越界
    # 越界检查

    if page * 10 >= groups.count():
        res = {"code": 401, "message": "用户组列表获取失败，页码越界"}
        return JsonResponse(res)

    if (page + 1) * 10 > groups.count():
        groups = groups.order_by('name')[10 * page:]
    else:
        groups = groups.order_by('name')[10 * page:10 * (page + 1)]

    # 返回用户组相关信息

    res = {"code": 200, "message": "用户组列表获取成功", "data": [{"name": group.name, "description": group.description, "creator": group.created_by.name, "create_time": group.created_at, "members": [user.username for user in group.members.all()]} for group in groups]}
    return JsonResponse(res)

