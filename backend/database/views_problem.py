from django.views.decorators.http import require_http_methods
from django.db.models import F, Q

from .models import User, Group, ProblemGroup, Problem, ProblemPermission, Tag, Record, TemporaryProblemGroup
from .errors import *

# 定义一个函数，用于获取问题组
def _get_problem_group(request, permission):
    # 获取请求中的用户名和问题组id
    username = request.POST.get('username')
    problem_group_id = request.POST.get('problem_group_id')

    # 检查问题组是否存在
    check = ProblemGroup.objects.filter(id=problem_group_id)
    if not check:
        return E_PROBLEM_GROUP_NOT_FIND
    problem_group = check[0]

    # 如果用户名不是问题组的用户，则检查用户是否存在
    if username != problem_group.user.username:
        check = User.objects.filter(username=username)
        if not check:
            return E_USER_NOT_FIND
        user = check[0]

        # 检查用户是否有权限
        groups = user.groups.all()
        if not ProblemPermission.objects.filter(group__isnull=True, problem_group=problem_group,
                                                permission__gte=permission).exists() and not ProblemPermission.objects.filter(
            group__in=groups,
            problem_group=problem_group, permission__gte=permission).exists():
            return E_PERMISSION_DENIED

    return problem_group


def __get_problem(user, problem_id, permission):
    # 对 permission 参数，1 题目上传者和问题组管理者 2 题目上传者
    # 题目上传者和问题组管理者可以删除该题目
    # 仅题目上传者可修改该题目

    check = Problem.objects.filter(id=problem_id)
    if not check:
        return E_PROBLEM_NOT_FIND
    problem = check[0]
    problem_group = problem.problem_group

    if permission >= 2 and user != problem.creator:
        return E_PERMISSION_DENIED

    if permission <= 1 and user != problem.creator and user != problem_group.user:

        groups = user.groups.all()
        if not ProblemPermission.objects.filter(group__isnull=True, problem_group=problem_group,
                                                permission__gte=permission).exists() and not ProblemPermission.objects.filter(
            group__in=groups,
            problem_group=problem_group, permission__gte=permission).exists():
            return E_PERMISSION_DENIED

    return problem_group, problem


def _get_problem(request, permission):
    # 获取请求中的用户名和问题id
    username = request.POST.get('username')
    problem_id = request.POST.get('problem_id')

    # 查询数据库中是否存在该用户
    check = User.objects.filter(username=username)
    if not check:
        # 如果不存在，返回用户未找到错误
        return E_USER_NOT_FIND
    user = check[0]

    # 调用__get_problem函数，返回问题
    return __get_problem(user, problem_id, permission)


def _get_and_create_tags(request):
    tag_names = request.POST.getlist('tags[]')

    tags_to_add = []
    for tag_name in tag_names:
        check = Tag.objects.filter(name=tag_name)
        if check:
            tag = check[0]
        else:
            tag = Tag.objects.create(name=tag_name)
        tags_to_add.append(tag)

    return tags_to_add


@require_http_methods(["POST"])
def problem_group_create(request):
    username = request.POST.get('username')
    title = request.POST.get('title')
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

    problem_group = ProblemGroup.objects.create(user=check[0], title=title, description=description)

    if 'tags[]' in request.POST:
        tags = _get_and_create_tags(request)
        problem_group.tags.set(tags)

    return success_data("问题组创建成功", problem_group.id)


@require_http_methods(["POST"])
def problem_group_update(request):
    problem_group = _get_problem_group(request, 1)
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
def problem_group_delete(request):
    problem_group = _get_problem_group(request, 2)
    if isinstance(problem_group, JsonResponse):
        return problem_group

    problem_group.delete()
    return success("问题组删除成功")


@require_http_methods(["POST"])
def problem_share(request):
    problem_group = _get_problem_group(request, 1)
    if isinstance(problem_group, JsonResponse):
        return problem_group

    user = User.objects.get(username=request.POST.get('username'))
    group_name = request.POST.get('group_name')
    if group_name:
        group = Group.objects.filter(name=group_name)
        if not group:
            return E_GROUP_NOT_FIND
        group = group[0]

        if user not in group.members.all():
            return E_USER_NOT_IN_GROUP
    else:
        group = None

    newpermission = int(request.POST.get('permission'))
    check = ProblemPermission.objects.filter(group=group, problem_group=problem_group)
    if check:
        permission = check[0]
    else:
        permission = ProblemPermission.objects.create(group=group, problem_group=problem_group, permission=-1)

    if permission.permission >= newpermission:
        return E_PERMISSION_REPEAT

    permission.permission = newpermission
    permission.save()
    return success("问题组分享成功")


@require_http_methods(["POST"])
def problem_create(request):
    problem_group = _get_problem_group(request, 1)
    if isinstance(problem_group, JsonResponse):
        return problem_group

    user = User.objects.get(username=request.POST.get('username'))
    title = request.POST.get('title')
    type = request.POST.get('type')
    content = request.POST.get('content')
    ans_count = int(request.POST.get('ans_count'))
    title = title if title else content[:30]

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

    problem = Problem.objects.create(problem_group=problem_group, index=index, type=type, title=title, content=content,
                                     ans_count=ans_count, answer=answer,
                                     field1=field[0], field2=field[1], field3=field[2], field4=field[3],
                                     field5=field[4],
                                     field6=field[5], field7=field[6],
                                     creator=user)
    if 'tags[]' in request.POST:
        tags = _get_and_create_tags(request)
        problem.tags.set(tags)

    problem_group.problem_num = index
    problem_group.save()

    return success_data("题目创建成功", problem.id)


@require_http_methods(["POST"])
def problem_update(request):
    res = _get_problem(request, 2)
    if isinstance(res, JsonResponse):
        return res

    problem = res[1]
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
            return E_ILLIGAL_ANSWER

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
        tags = _get_and_create_tags(request)
        problem.tags.set(tags)

    return success("题目修改成功")


@require_http_methods(["POST"])
def problem_delete(request):
    res = _get_problem(request, 1)
    if isinstance(res, JsonResponse):
        return res

    problem_group, problem = res
    index = problem.index
    problem.delete()

    Problem.objects.filter(problem_group=problem_group, index__gt=index).update(index=F('index') - 1)
    problem_group.problem_num -= 1
    problem_group.save()
    return success("题目删除成功")


@require_http_methods(["POST"])
def problem_adjust_order(request):
    res = _get_problem(request, 1)
    if isinstance(res, JsonResponse):
        return res

    problem_group, problem = res
    index = problem.index
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
    return success("题目顺序更改成功")


def _cut_to_page(request, query_set):
    page = request.POST.get('page')
    number_per_page = request.POST.get('number_per_page')
    if not page or not number_per_page:
        return query_set

    page = int(page) - 1
    number_per_page = int(number_per_page)

    if page < 0 or page * number_per_page >= query_set.count():
        return E_PAGE_OVERFLOW
    
    # python 切片不会引发索引越界错误
    query_set = query_set[number_per_page * page:number_per_page * (page + 1)]

    return query_set


def _problem_group_to_dict(problem_group):
    return {
        'id': problem_group.id,
        'title': problem_group.title,
        'creator': problem_group.user.username,
        'description': problem_group.description,
        'tags': [tag.name for tag in problem_group.tags.all()],
        'problem_num': problem_group.problem_num,
    }


def _problem_groups_to_list(problem_groups):
    result = []
    for problem_group in problem_groups:
        result.append(_problem_group_to_dict(problem_group))
    return result

def _get_problem_groups_with_permissions__gte(user, group_name, permission):
    if group_name == '_created_by_self':
        problem_groups = ProblemGroup.objects.filter(user=user)
    else:
        if group_name == '_shared_to_all':
            permissions = ProblemPermission.objects.filter(group__isnull=True, permission__gte=permission)
        elif group_name:
            group = Group.objects.filter(name=group_name)
            if not group:
                return E_GROUP_NOT_FIND
            group = group[0]

            if not user in group.members.all():
                return E_USER_NOT_IN_GROUP

            permissions = ProblemPermission.objects.filter(group=group, permission__gte=permission)
        else:
            groups = user.groups.all()
            query = Q(group__isnull=True) | Q(group__in=groups)
            permissions = ProblemPermission.objects.filter(query, permission__gte=permission)
        problem_group_ids = permissions.values_list('problem_group', flat=True)

        query = Q(id__in=problem_group_ids)
        if not group_name:
            query |= Q(user=user)

        problem_groups = ProblemGroup.objects.filter(query)

    return problem_groups

@require_http_methods(["POST"])
def get_problem_groups_num(request):
    # 获取请求中的username
    username = request.POST.get('username')
    # 根据username获取User对象
    user = User.objects.get(username=username)
    # 如果User对象不存在，返回错误信息
    if not user:
        return E_USER_NOT_FIND

    # 获取请求中的mode
    mode = int(request.POST.get('mode'))
    filter_group = request.POST.get('filter_group')

    if mode:
        problem_groups = _get_problem_groups_with_permissions__gte(user, filter_group, 1)
        if isinstance(problem_groups, JsonResponse):
            return problem_groups
    else:
        problem_groups = _get_problem_groups_with_permissions__gte(user, '', 1)
        if isinstance(problem_groups, JsonResponse):
            return problem_groups
        
        exclude_ids = problem_groups.values_list('id', flat=True)
        problem_groups = _get_problem_groups_with_permissions__gte(user, filter_group, 0)
        if isinstance(problem_groups, JsonResponse):
            return problem_groups
        
        problem_groups = problem_groups.exclude(id__in=exclude_ids)

    return success_data("问题组数量查询成功", problem_groups.count())


@require_http_methods(["POST"])
def get_problem_groups(request):
    # 获取请求中的username
    username = request.POST.get('username')
    # 根据username获取User对象
    user = User.objects.get(username=username)
    # 如果User对象不存在，返回错误信息
    if not user:
        return E_USER_NOT_FIND

    mode = int(request.POST.get('mode'))
    filter_group = request.POST.get('filter_group')
 
    if mode:
        problem_groups = _get_problem_groups_with_permissions__gte(user, filter_group, 1)
        if isinstance(problem_groups, JsonResponse):
            return problem_groups
    else:
        problem_groups = _get_problem_groups_with_permissions__gte(user, '', 1)
        if isinstance(problem_groups, JsonResponse):
            return problem_groups
        
        exclude_ids = problem_groups.values_list('id', flat=True)
        problem_groups = _get_problem_groups_with_permissions__gte(user, filter_group, 0)
        if isinstance(problem_groups, JsonResponse):
            return problem_groups
        
        problem_groups = problem_groups.exclude(id__in=exclude_ids)


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


def _get_problems_with_permissions(user, group_name):
    problem_groups = _get_problem_groups_with_permissions__gte(user, group_name, 0)
    if isinstance(problem_groups, JsonResponse):
        return problem_groups

    problems = Problem.objects.filter(problem_group__in=problem_groups)
    return problems


def _problem_to_dict(user, problem):
    all_record = Record.objects.filter(problem=problem)
    all_right_record = all_record.filter(result=True)
    user_record = all_record.filter(user=user)
    user_right_record = user_record.filter(result=True)
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

        # 用于展示用户是否做过此题（user_count）并计算个人正确率、总正确率
        'user_right_count': user_right_record.count(),
        'user_count': user_record.count(),
        'all_right_count': all_right_record.count(),
        'all_count': all_record.count(),
    }


def _problems_to_list(user, problems):
    result = []
    for problem in problems:
        result.append(_problem_to_dict(user, problem))
    return result


@require_http_methods(["POST"])
def get_problem_num_with_permissions(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return E_USER_NOT_FIND
    user = user[0]

    filter_group = request.POST.get('filter_group')
    problems = _get_problems_with_permissions(user, filter_group)
    if isinstance(problems, JsonResponse):
        return problems

    return success_data("问题数量查询成功", problems.count())


@require_http_methods(["POST"])
def get_problems_with_permissions(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return E_USER_NOT_FIND
    user = user[0]

    filter_group = request.POST.get('filter_group')
    problems = _get_problems_with_permissions(user, filter_group)
    if isinstance(problems, JsonResponse):
        return problems

    if not problems:
        return E_NO_PROBLEM

    problems = _cut_to_page(request, problems)
    if isinstance(problems, JsonResponse):
        return problems

    return success_data("问题查询成功", _problems_to_list(user, problems))


@require_http_methods(["POST"])
def temporary_problem_group_create(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return E_USER_NOT_FIND
    user = user[0]

    problem_ids = request.POST.getlist('problem_ids[]')
    problem_list = []
    for id in problem_ids:
        problem = __get_problem(user, int(id), 0)
        if isinstance(problem, JsonResponse):
            return problem

        problem_list.append(problem[1])

    temp_group = TemporaryProblemGroup.objects.create(user=user)
    temp_group.problems.set(problem_list)
    return success_data("临时问题组创建成功", temp_group.id)


def temporary_problem_group_clear(user):
    TemporaryProblemGroup.objects.filter(user=user).delete()


@require_http_methods(["POST"])
def get_problem_group_content(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return E_USER_NOT_FIND
    user = user[0]

    is_temporary = request.POST.get('is_temporary')
    if is_temporary == 'y':
        group_id = request.POST.get('problem_group_id')
        temp_group = TemporaryProblemGroup.objects.filter(id=group_id)
        if not temp_group:
            return E_PROBLEM_GROUP_NOT_FIND
        temp_group = temp_group[0]

        if user != temp_group.user:
            return E_PERMISSION_DENIED

        problems = temp_group.problems.all()
    else:
        problem_group = _get_problem_group(request, 0)
        if isinstance(problem_group, JsonResponse):
            return problem_group

        problems = Problem.objects.filter(problem_group=problem_group)
        problems = problems.order_by('index')

    if not problems:
        return E_NO_PROBLEM

    problems = _cut_to_page(request, problems)
    if isinstance(problems, JsonResponse):
        return problems

    return success_data("问题组内容获取成功", _problems_to_list(user, problems))


@require_http_methods(["POST"])
def get_single_problem_group_detail(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return E_USER_NOT_FIND
    user = user[0]

    is_temporary = request.POST.get('is_temporary')
    if is_temporary == 'y':
        group_id = request.POST.get('problem_group_id')
        temp_group = TemporaryProblemGroup.objects.filter(id=group_id)
        if not temp_group:
            return E_PROBLEM_GROUP_NOT_FIND
        temp_group = temp_group[0]

        if user != temp_group.user:
            return E_PERMISSION_DENIED

        problem_num = temp_group.problems.count()
        data = {'problem_num': problem_num}
    else:
        problem_group = _get_problem_group(request, 0)
        if isinstance(problem_group, JsonResponse):
            return problem_group

        data = _problem_group_to_dict(problem_group)

    return success_data("问题组详情查询成功", data)


@require_http_methods(["POST"])
def get_single_problem_detail(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return E_USER_NOT_FIND
    user = user[0]

    res = _get_problem(request, 0)
    if isinstance(res, JsonResponse):
        return res

    data = _problem_to_dict(user, res[1])

    return success_data("问题详情查询成功", data)


@require_http_methods(["POST"])
def problem_check(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return E_USER_NOT_FIND
    user = user[0]

    res = _get_problem(request, 0)
    if isinstance(res, JsonResponse):
        return res

    problem = res[1]
    ans_count = problem.ans_count
    if problem.type == 'c':
        user_answer = request.POST.get('user_answer')
        if not user_answer or len(user_answer) > 1 or ord(user_answer) - ord('A') not in range(ans_count):
            return E_ILLIGAL_ANSWER

        correct = 'T' if user_answer == problem.answer else 'F'
        data = {
            'correct': correct,
            'answer': problem.answer,
        }
    else:
        correct = 'T'
        field = [problem.field1, problem.field2, problem.field3, problem.field4, problem.field5, problem.field6,
                 problem.field7]
        correct_detail = ['' for _ in range(7)]
        for i in range(ans_count):
            if request.POST.get('user_field' + str(i + 1)).strip() == field[i].strip():
                correct_detail[i] = 'T'
            else:
                correct_detail[i] = 'F'
                correct = 'F'

        data = {
            'correct': correct,
        }
        for i in range(7):
            data.update({
                'field' + str(i + 1): field[i],
                'correct' + str(i + 1): correct_detail[i],
            })

    Record.objects.create(user=user, problem=problem, result=(correct == 'T'))

    all_record = Record.objects.filter(problem=problem)
    all_right_record = all_record.filter(result=True)
    user_record = all_record.filter(user=user)
    user_right_record = user_record.filter(result=True)
    data.update({
        'user_right_count': user_right_record.count(),
        'user_count': user_record.count(),
        'all_right_count': all_right_record.count(),
        'all_count': all_record.count(),
    })
    return success_data("判题成功", data)

# @require_http_methods(["POST"])
# # 高级搜索问题
# def problem_search_advanced(request):
#     username = request.POST.get("username")
#     problems = _get_problems_with_permissions(username)
#     if isinstance(problems, JsonResponse):
#         return problems

#     use_regex = request.POST.get("use_regex")
#     use_regex = use_regex == "true"
#     pattern = request.POST.get("pattern")
#     keywords = request.POST.get("keywords").split(" ")
#     result = QuerySet()

#     if not use_regex:
#         for keyword in keywords:
#             result.union(problems.all().objects.search(keyword))
#     else:
#         result = problems.all().objects.search_regex(pattern)
#     return success(result)


# data = [
#     {
#         "id": 1,
#         "problem_title": "如何计算矩阵的行列式？",
#         "problem_group_title": "Math Questions",
#         "problem_group_id": 101,
#         "tags": ["矩阵", "行列式"],
#         "creator": "user123",
#         "user_right_count": 5,
#         "user_count": 10,
#         "all_right_count": 150,
#         "all_count": 300,
#     },
#     {
#         "id": 2,
#         "problem_title": "求解线性方程组的解",
#         "problem_group_title": "Math Questions",
#         "problem_group_id": 101,
#         "tags": ["线性代数", "方程组"],
#         "creator": "user456",
#         "user_right_count": 3,
#         "user_count": 8,
#         "all_right_count": 200,
#         "all_count": 400,
#     },
# ]


# # 视图函数
# @require_http_methods(["POST"])
# def get_problems_fake(request):
#     # 构建成功响应的数据结构
#     response_data = {
#         "code": 200,
#         "message": "问题查询成功",
#         "data": data
#     }
#     return JsonResponse(response_data, safe=False)  # 使用safe=False允许返回非字典类型的数据
