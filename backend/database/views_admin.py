from django.views.decorators.http import require_http_methods
from django.db.models import F

from .errors import *
from .models import User, Group, ProblemGroup, Problem, Record, TemporaryProblemGroup
from .views_problem import _get_problem_groups_with_permissions__gte, _cut_to_page, _problem_groups_to_list, \
    _get_and_create_tags, _get_problems_with_permissions


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

    if check[0] in check2[0].members.all():
        res = {"code": 402, "message": "用户已经在该用户组中"}
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

    if not check[0] in check2[0].members.all():
        res = {"code": 402, "message": "用户不在该用户组中"}
        return JsonResponse(res)

    check2[0].members.remove(check[0])
    if check2[0].created_by == check[0]:
        check2[0].delete()
        res = {"code": 200, "message": "踢出群主，群已解散成功"}
        return JsonResponse(res)

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
def admin_get_user_list(request):
    users = User.objects.all()
    users = _cut_to_page(request, users)

    if isinstance(users, JsonResponse):
        return users

    # 返回用户相关信息
    res = {"code": 200, "message": "用户列表获取成功", "data": [
        {"username": user.username, "password": user.password,
         "groups": [group.name for group in user.groups.all()]} for user in users]}
    return JsonResponse(res)


@require_http_methods(["POST"])
def admin_get_user_list_num(request):
    users = User.objects.all()
    res = {"code": 200, "message": "用户列表获取成功", "data": users.count()}
    return JsonResponse(res)


@require_http_methods(["POST"])
# 管理员获得第 i 页的用户组名单
def admin_get_group_list(request):
    groups = Group.objects.all()
    groups = _cut_to_page(request, groups)

    if isinstance(groups, JsonResponse):
        return groups

    # 返回用户组相关信息
    res = {"code": 200, "message": "用户组列表获取成功", "data": [
        {"name": group.name, "description": group.description, "creator": group.created_by.username,
         "create_time": group.created_at, "members": [user.username for user in group.members.all()]} for group in
        groups]}
    return JsonResponse(res)


@require_http_methods(["POST"])
def admin_get_group_list_num(request):
    groups = Group.objects.all()
    res = {"code": 200, "message": "用户组列表获取成功", "data": groups.count()}
    return JsonResponse(res)


@require_http_methods(["POST"])
def admin_get_problem_groups(request):
    problem_groups = ProblemGroup.objects.all()

    creator = request.POST.get('username_to_search')
    to_search = request.POST.get('to_search')
    if creator:
        creator = User.objects.get(username=creator)
        if not creator:
            return E_USER_NOT_FIND

        mode = int(request.POST.get('mode'))
        filter_group = request.POST.get('filter_group')

        if mode:
            problem_groups = _get_problem_groups_with_permissions__gte(creator, filter_group, 1)
            if isinstance(problem_groups, JsonResponse):
                return problem_groups
        else:
            problem_groups = _get_problem_groups_with_permissions__gte(creator, '', 1)
            if isinstance(problem_groups, JsonResponse):
                return problem_groups

            exclude_ids = problem_groups.values_list('id', flat=True)
            problem_groups = _get_problem_groups_with_permissions__gte(creator, filter_group, 0)
            if isinstance(problem_groups, JsonResponse):
                return problem_groups

            problem_groups = problem_groups.exclude(id__in=exclude_ids)

    if to_search:
        # 在 problem_groups 范围内进一步搜索，利用 search
        problem_groups = problem_groups.search(to_search)

    # 如果问题组不存在，返回错误信息
    if not problem_groups:
        return E_NO_PROBLEM_GROUP

    # 调用_cut_to_page函数，分页问题组
    problem_groups = _cut_to_page(request, problem_groups)
    # 如果返回的是JsonResponse，直接返回
    if isinstance(problem_groups, JsonResponse):
        return problem_groups

    # 返回成功信息，以及问题组列表
    return success_data("问题组查询成功", _problem_groups_to_list(problem_groups))


def _admin_get_problem_group(request):
    problem_group_id = request.POST.get('problem_group_id')

    # 检查问题组是否存在
    check = ProblemGroup.objects.filter(id=problem_group_id)
    if not check:
        return E_PROBLEM_GROUP_NOT_FIND
    problem_group = check[0]

    return problem_group


@require_http_methods(["POST"])
def admin_problem_group_update(request):
    problem_group = _admin_get_problem_group(request)
    if isinstance(problem_group, JsonResponse):
        return problem_group

    newtitle = request.POST.get('title')
    newtitle = newtitle if newtitle else problem_group.title
    if len(newtitle) > 50:
        return E_TITLE_FORMAT

    if 'description' in request.POST:
        description = request.POST.get('description')
    else:
        description = problem_group.description

    if len(description) > 200:
        return E_DESCRIPTION_FORMAT

    problem_group.title = newtitle
    problem_group.description = description
    problem_group.save()

    if 'tags[]' in request.POST:
        tags = _get_and_create_tags(request)
        problem_group.tags.set(tags)

    return success("问题组修改成功")


@require_http_methods(["POST"])
def admin_problem_group_delete(request):
    problem_group = _admin_get_problem_group(request)
    if isinstance(problem_group, JsonResponse):
        return problem_group

    problem_group.delete()

    return success("问题组删除成功")


def _admin_problem_to_dict(problem):
    all_record = Record.objects.filter(problem=problem)
    all_right_record = all_record.filter(result=True)
    return {
        'id': problem.id,
        'type': problem.type,
        'problem_title': problem.title,
        'content': problem.content,
        'ans_count': problem.ans_count,
        'answer': problem.answer,
        'field1': problem.field1,
        'field2': problem.field2,
        'field3': problem.field3,
        'field4': problem.field4,
        'field5': problem.field5,
        'field6': problem.field6,
        'field7': problem.field7,
        'tags': [tag.name for tag in problem.tags.all()],
        'creator': problem.creator.username,

        'problem_group_id': problem.problem_group.id,
        'problem_group_title': problem.problem_group.title,

        'all_right_count': all_right_record.count(),
        'all_count': all_record.count(),
    }


def _admin_problems_to_list(problems):
    result = []
    for problem in problems:
        result.append(_admin_problem_to_dict(problem))
    return result


@require_http_methods(["POST"])
def admin_get_problems(request):
    problems = Problem.objects.all()
    creator = request.POST.get('username_to_search')
    if creator:
        creator = User.objects.filter(username=creator)

        if not creator:
            return E_USER_NOT_FIND

        creator = creator[0]

        filter_group = request.POST.get('filter_group')
        problems = _get_problems_with_permissions(creator, filter_group)
        if isinstance(problems, JsonResponse):
            return problems

        if not problems:
            return E_NO_PROBLEM

    to_search = request.POST.get('to_search')
    if to_search:
        problems = problems.search(to_search)

    if not problems:
        return E_NO_PROBLEM

    problems = _cut_to_page(request, problems)
    if isinstance(problems, JsonResponse):
        return problems

    return success_data("问题查询成功", _admin_problems_to_list(problems))


@require_http_methods(["POST"])
def admin_problem_delete(request):
    problem_id = request.POST.get('problem_id')
    problem = Problem.objects.filter(id=problem_id)
    if not problem:
        return E_PROBLEM_NOT_FIND

    problem = problem[0]
    index = problem.index
    problem_group = problem.problem_group
    problem.delete()

    Problem.objects.filter(problem_group=problem_group, index__gt=index).update(index=F('index') - 1)
    problem_group.problem_num -= 1
    problem_group.save()
    return success("题目删除成功")


@require_http_methods(["POST"])
def admin_problem_update(request):
    problem_id = request.POST.get('problem_id')
    problem = Problem.objects.filter(id=problem_id)
    if not problem:
        return E_PROBLEM_NOT_FIND

    problem = problem[0]
    title = request.POST.get('title')
    title = title if title else problem.title
    type = request.POST.get('type')
    type = type if type else problem.type
    content = request.POST.get('content')
    content = content if content else problem.content
    ans_count = request.POST.get('ans_count')
    ans_count = int(ans_count) if ans_count else problem.ans_count

    if type not in ['c', 'b']:
        return E_UNKNOWN_TYPE
    if len(content) > 1000:
        return E_PROBLEM_CONTENT_FORMAT
    if ans_count > 7:
        return E_PROBLEM_OPTIONS_OR_BLANK_TOO_MUCH

    answer = ''
    if type == 'c':
        answer = request.POST.get('answer')
        answer = answer if answer else problem.answer
        if len(answer) > 1 or ord(answer) - ord('A') not in range(ans_count):
            return E_ILLEGAL_ANSWER

    field = ['' for _ in range(7)]
    pre_field = [problem.field1, problem.field2, problem.field3,
                 problem.field4, problem.field5, problem.field6, problem.field7]
    for i in range(ans_count):
        field[i] = request.POST.get('field' + str(i + 1))
        field[i] = field[i] if field[i] else pre_field[i]
        if len(field[i]) > 100:
            return E_PROBLEM_OPTIONS_OR_BLANK_FORMAT

    problem.type, problem.title, problem.content, problem.ans_count, problem.answer = type, title, content, ans_count, answer
    problem.field1, problem.field2, problem.field3, problem.field4, problem.field5, problem.field6, problem.field7 = field
    problem.save()

    if 'tags[]' in request.POST:
        print([tag.name for tag in problem.tags.all()])
        tags = _get_and_create_tags(request)
        problem.tags.set(tags)
        print([tag.name for tag in problem.tags.all()])

    return success("题目修改成功")


@require_http_methods(["POST"])
def admin_get_problem_group_content(request):

    is_temporary = request.POST.get('is_temporary')
    if is_temporary == 'y':
        group_id = request.POST.get('problem_group_id')
        temp_group = TemporaryProblemGroup.objects.filter(id=group_id)
        if not temp_group:
            return E_PROBLEM_GROUP_NOT_FIND
        temp_group = temp_group[0]

        problems = temp_group.problems.all()
    else:
        problem_group = _admin_get_problem_group(request)
        if isinstance(problem_group, JsonResponse):
            return problem_group

        problems = Problem.objects.filter(problem_group=problem_group)
        problems = problems.order_by('index')

    if not problems:
        return E_NO_PROBLEM

    problems = _cut_to_page(request, problems)
    if isinstance(problems, JsonResponse):
        return problems

    return success_data("问题组内容获取成功", _admin_problems_to_list(problems))
