from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import F, QuerySet

from .models import User, ProblemGroup, Problem

E_USER_NOT_FIND = JsonResponse(
    {"code": 401, "message": "用户不存在"})  # 当前用户 username 或问题组创建者 problem_group_creator 不存在
E_PROBLEM_GROUP_REPEAT = JsonResponse({"code": 402, "message": "问题组已存在"})
E_PROBLEM_GROUP_NOT_FIND = JsonResponse({"code": 402, "message": "问题组不存在"})
E_PERMISSON_DENIED = JsonResponse({"code": 403, "message": "当前用户没有权限"})
E_PROBLEM_NOT_FIND = JsonResponse({"code": 405, "message": "问题不存在"})
E_TITLE_FORMAT = JsonResponse({"code": 406, "message": "标题非空且长度不能超过50"})
E_DESCRIPTION_FORMAT = JsonResponse({"code": 406, "message": "描述长度不能超过200"})
E_UNKNOWN_TYPE = JsonResponse({"code": 407, "message": "未知题目类型"})
E_PROBLEM_CONTENT_FORMAT = JsonResponse({"code": 407, "message": "题干非空且长度不能超过1000"})
E_PROBLEM_OPTIONS_OR_BLANK_TOO_MUCH = JsonResponse({"code": 407, "message": "选项或填空数量不能超过7"})
E_ILLIGAL_ANSWER = JsonResponse({"code": 407, "message": "答案不合法"})
E_PROBLEM_OPTIONS_OR_BLANK_FORMAT = JsonResponse({"code": 407, "message": "选项或填空内容非空且长度不能超过100"})
E_BAD_POS = JsonResponse({"code": 408, "message": "题目位置不合法"})


def _success(text):
    return JsonResponse({"code": 200, "message": text})


def _get_problem_group(request, permisson):  # 0 仅可查看，1 可查看并添加问题，2 全部权限
    username = request.POST.get('username')
    problem_group_creator = request.POST.get('problem_group_creator')
    problem_group_title = request.POST.get('problem_group_title')

    check = User.objects.filter(username=problem_group_creator)
    if not check:
        return E_USER_NOT_FIND

    check = ProblemGroup.objects.filter(user=check[0], title=problem_group_title)
    if not check:
        return E_PROBLEM_GROUP_NOT_FIND

    problem_group = check[0]

    if permisson >= 0 and username != problem_group_creator:
        check = User.objects.filter(username=username)
        if not check:
            return E_USER_NOT_FIND

        # TODO

        return E_PERMISSON_DENIED

    return problem_group


def _get_problem(request, group_permisson, permisson):
    # 对 permisson 参数，同上
    # 对 permisson 参数，0 仅可查看，1 可查看/删除，2 可查看/删除/修改
    # 对该问题组有查看权限同样对该问题有查看权限
    # 题目上传者和问题组拥有者可以删除该题目
    # 仅题目上传者可修改该题目
    problem_group = _get_problem_group(request, group_permisson)
    if isinstance(problem_group, JsonResponse):
        return problem_group

    username = request.POST.get('username')
    index = int(request.POST.get('index'))
    check = Problem.objects.filter(problem_group=problem_group, index=index)
    if not check:
        return E_PROBLEM_NOT_FIND
    problem = check[0]

    if permisson >= 2 and username != problem.creator.username:
        return E_PERMISSON_DENIED

    if permisson == 1 and username != problem.creator.username and username != problem_group.user.username:
        return E_PERMISSON_DENIED

    return problem_group, problem


@require_http_methods(["POST"])
def problem_group_create(request):
    username = request.POST.get('username')
    title = request.POST.get('problem_group_title')
    description = request.POST.get('description')
    description = description if description else ''

    check = User.objects.filter(username=username)
    if not check:
        return E_USER_NOT_FIND

    if not title or len(title) > 50:
        return E_TITLE_FORMAT

    if len(description) > 200:
        return E_DESCRIPTION_FORMAT

    if ProblemGroup.objects.filter(user=check[0], title=title).exists():
        return E_PROBLEM_GROUP_REPEAT

    ProblemGroup.objects.create(user=check[0], title=title, description=description)
    return _success("问题组创建成功")


@require_http_methods(["POST"])
def problem_group_update(request):
    problem_group = _get_problem_group(request, 2)
    if isinstance(problem_group, JsonResponse):
        return problem_group

    newtitle = request.POST.get('newtitle')
    newtitle = newtitle if newtitle else problem_group.title
    if len(newtitle) > 50:
        return E_TITLE_FORMAT

    description = request.POST.get('newdescription')
    description = description if description is not None else problem_group.description
    if len(description) > 200:
        return E_DESCRIPTION_FORMAT

    problem_group.title = newtitle
    problem_group.description = description
    problem_group.save()
    return _success("问题组修改成功")


@require_http_methods(["POST"])
def problem_group_delete(request):
    problem_group = _get_problem_group(request, 2)
    if isinstance(problem_group, JsonResponse):
        return problem_group

    problem_group.delete()
    return _success("问题组删除成功")


@require_http_methods(["POST"])
def problem_create(request):
    problem_group = _get_problem_group(request, 1)
    user = User.objects.get(username=request.POST.get('username'))
    type = request.POST.get('type')
    content = request.POST.get('content')
    ans_count = int(request.POST.get('ans_count'))

    if type not in ['c', 'b']:
        return E_UNKNOWN_TYPE
    if not content or len(content) > 1000:
        return E_PROBLEM_CONTENT_FORMAT
    if ans_count > 7:
        return E_PROBLEM_OPTIONS_OR_BLANK_TOO_MUCH

    answer = ''
    if type == 'c':
        answer = request.POST.get('answer')
        if not answer or len(answer) > 1 or ord(answer) - ord('A') not in range(ans_count):
            return E_ILLIGAL_ANSWER

    field = ['' for _ in range(7)]
    for i in range(ans_count):
        field[i] = request.POST.get('field' + str(i + 1))
        if not field[i] or len(field[i]) > 100:
            return E_PROBLEM_OPTIONS_OR_BLANK_FORMAT

    index = problem_group.problem_num + 1
    title = content[:30]
    Problem.objects.create(problem_group=problem_group, index=index, type=type, content=content, ans_count=ans_count,
                           answer=answer, title=title,
                           field1=field[0], field2=field[1], field3=field[2], field4=field[3], field5=field[4],
                           field6=field[5], field7=field[6],
                           creator=user)

    problem_group.problem_num = index
    problem_group.save()

    return _success("题目创建成功")


@require_http_methods(["POST"])
def problem_update(request):
    res = _get_problem(request, -1, 2)
    if isinstance(res, JsonResponse):
        return res

    problem_group, problem = res
    type = request.POST.get('type')
    type = type if type else problem.type
    content = request.POST.get('content')
    content = content if content else problem.content
    ans_count = request.POST.get('ans_count')
    ans_count = int(ans_count) if ans_count else problem.ans_count
    title = request.POST.get('title')
    title = title if title else problem.title

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
            return E_ILLIGAL_ANSWER

    field = ['' for _ in range(7)]
    pre_field = [problem.field1, problem.field2, problem.field3,
                 problem.field4, problem.field5, problem.field6, problem.field7]
    for i in range(ans_count):
        field[i] = request.POST.get('field' + str(i + 1))
        field[i] = field[i] if field[i] else pre_field[i]
        if len(field[i]) > 100:
            return E_PROBLEM_OPTIONS_OR_BLANK_FORMAT

    problem.title = title
    problem.type, problem.content, problem.ans_count, problem.answer = type, content, ans_count, answer
    problem.field1, problem.field2, problem.field3, problem.field4, problem.field5, problem.field6, problem.field7 = field
    problem.save()
    return _success("题目修改成功")


@require_http_methods(["POST"])
def problem_delete(request):
    res = _get_problem(request, -1, 1)
    if isinstance(res, JsonResponse):
        return res

    problem_group, problem = res
    problem.delete()

    index = int(request.POST.get("index"))
    Problem.objects.filter(problem_group=problem_group, index__gt=index).update(index=F('index') - 1)
    problem_group.problem_num -= 1
    problem_group.save()
    return _success("题目删除成功")


@require_http_methods(["POST"])
def problem_adjust_order(request):
    res = _get_problem(request, 2, -1)
    if isinstance(res, JsonResponse):
        return res

    problem_group, problem = res
    index = int(request.POST.get("index"))
    newindex = int(request.POST.get("newindex"))
    maxindex = problem_group.problem_num
    if newindex < 1 or newindex > maxindex:
        return E_BAD_POS

    if newindex < index:
        Problem.objects.filter(problem_group=problem_group, index__gte=newindex, index__lt=index).update(
            index=F('index') + 1)
    elif newindex > index:
        Problem.objects.filter(problem_group=problem_group, index__gt=index, index__lte=newindex).update(
            index=F('index') - 1)

    problem.index = newindex
    problem.save()
    return _success("题目顺序更改成功")


# 获取用户有权限的所有问题
def _get_problems_with_permissions(username: str) -> JsonResponse | QuerySet[Problem]:
    user = User.objects.get(username=username)
    if not user:
        return E_USER_NOT_FIND
    else:
        user = user[0]
    groups = user.groups.all()

    if not groups:
        return JsonResponse({"code": 402, "msg": "用户不在任何组中"})

    permissions = [group.permissions.all() for group in groups]
    problem_groups = [per.problem_group.all() for per in permissions]

    if not problem_groups:
        return JsonResponse({"code": 403, "msg": "用户没有权限查看任何题目组"})

    # 问题组合并到一个QuerySet
    total_problem_groups = problem_groups[0].union(*problem_groups[1:]) if len(problem_groups) > 1 else problem_groups[
        0]

    problems = QuerySet()

    # 获取所有问题并合并到一个 QuerySet
    for problem_group in total_problem_groups:
        problems.union(Problem.objects.filter(problem_group=problem_group))

    return problems


@require_http_methods(["POST"])
# 高级搜索问题
def problem_search_advanced(request):
    username = request.POST.get("username")
    problems = _get_problems_with_permissions(username)
    if isinstance(problems, JsonResponse):
        return problems

    use_regex = request.POST.get("use_regex")
    use_regex = use_regex == "true"
    pattern = request.POST.get("pattern")
    keywords = request.POST.get("keywords").split(" ")
    result = QuerySet()

    if not use_regex:
        for keyword in keywords:
            result.union(problems.all().objects.search(keyword))
    else:
        result = problems.all().objects.search_regex(pattern)
    return _success(result)
