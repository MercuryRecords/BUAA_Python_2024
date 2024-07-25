from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import F, Q, QuerySet

from .models import User, Group, ProblemGroup, Problem, ProblemPermission, Tag, Record

from .error import *

def _get_problem_group(request, permission):
    username = request.POST.get('username')
    problem_group_id = request.POST.get('problem_group_id')

    check = ProblemGroup.objects.filter(id=problem_group_id)
    if not check:
        return E_PROBLEM_GROUP_NOT_FIND
    problem_group = check[0]

    if permission >= 0 and username != problem_group.user.username:
        check = User.objects.filter(username=username)
        if not check:
            return E_USER_NOT_FIND
        user = check[0]

        groups = user.groups.all()
        if not ProblemPermission.objects.filter(group__isnull=True, problem_group=problem_group,
                permission__gte=permission).exists() and not ProblemPermission.objects.filter(group__in=groups,
                problem_group=problem_group, permission__gte=permission).exists():
            return E_PERMISSION_DENIED

    return problem_group


def _get_problem(request, permission):
    # 对 permission 参数，0 题目上传者和问题组管理者 1 题目上传者
    # 题目上传者和问题组管理者可以删除该题目
    # 仅题目上传者可修改该题目
    username = request.POST.get('username')
    problem_id = request.POST.get('problem_id')
    check = Problem.objects.filter(id=problem_id)
    if not check:
        return E_PROBLEM_NOT_FIND
    problem = check[0]
    problem_group = problem.problem_group

    if permission >= 1 and username != problem.creator.username:
        return E_PERMISSION_DENIED

    if permission == 0 and username != problem.creator.username and username != problem_group.user.username:
        check = User.objects.filter(username=username)
        if not check:
            return E_USER_NOT_FIND
        user = check[0]

        groups = user.groups.all()
        if not ProblemPermission.objects.filter(group__isnull=True, problem_group=problem_group,
                permission__gte=1).exists() and not ProblemPermission.objects.filter(group__in=groups,
                problem_group=problem_group, permission__gte=1).exists():
            return E_PERMISSION_DENIED
        
    return problem_group, problem


def _get_and_create_tags(request):
    tag_names = request.POST.getlist('tags')

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
    
    if 'tags' in request.POST:
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

    if 'tags' in request.POST:
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
    
    group_name = request.POST.get('group_name')
    if group_name:
        group = Group.objects.filter(name=group_name)
        if not group:
            return E_GROUP_NOT_FIND
        group = group[0]
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
                           field1=field[0], field2=field[1], field3=field[2], field4=field[3], field5=field[4],
                           field6=field[5], field7=field[6],
                           creator=user)
    if 'tags' in request.POST:
        tags = _get_and_create_tags(request)
        problem.tags.set(tags)

    problem_group.problem_num = index
    problem_group.save()

    return success_data("题目创建成功", problem.id)


@require_http_methods(["POST"])
def problem_update(request):
    res = _get_problem(request, 1)
    if isinstance(res, JsonResponse):
        return res

    problem_group, problem = res
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

    if 'tags' in request.POST:
        tags = _get_and_create_tags(request)
        problem.tags.set(tags)

    return success("题目修改成功")


@require_http_methods(["POST"])
def problem_delete(request):
    res = _get_problem(request, 0)
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
    res = _get_problem(request, 0)
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


def _cut_to_page(request, query_set, sort_key, reverse=''):
    page = int(request.POST.get('page')) - 1
    number_per_page = int(request.POST.get('number_per_page'))

    if page * number_per_page >= query_set.count():
        return E_PAGE_OVERFLOW

    if reverse != '-':
        reverse = ''
    object = object.order_by(reverse + sort_key)

    if (page + 1) * number_per_page >= query_set.count():
        query_set = query_set[number_per_page * page:]
    else:
        query_set = query_set[number_per_page * page:number_per_page * (page + 1)]

    return query_set


def _problem_groups_to_list(problem_groups):
    result = []
    for problem_group in problem_groups:
        result.append({
            'creator': problem_group.user,
            'title': problem_group.title,
            'description': problem_group.description,
            'tags': [tag.name for tag in problem_group.tags.all()],
            'problem_num': problem_group.problem_num,
        })
    return result


@require_http_methods(["POST"])
def get_created_problem_groups_num(request):
    username = request.POST.get('username')
    user = User.objects.get(username=username)
    if not user:
        return E_USER_NOT_FIND

    problem_groups = user.created_problem_groups.all()
    return success_data("问题组数量查询成功", problem_groups.count())


@require_http_methods(["POST"])
def get_created_problem_groups(request):
    username = request.POST.get('username')
    user = User.objects.get(username=username)
    if not user:
        return E_USER_NOT_FIND

    problem_groups = user.created_problem_groups.all()
    if not problem_groups:
        return E_NO_PROBLEM_GROUP

    problem_groups = _cut_to_page(request, problem_groups, "title")
    return success_data("问题组查询成功", _problem_groups_to_list(problem_groups))


def _get_problems_with_permissions(user, group):
    if group:
        permisson = ProblemPermission.objects.filter(group=group)
    else:
        groups = user.groups.all()
        query = Q(group__isnull=True) | Q(group__in=groups)
        permissions = ProblemPermission.objects.filter(query)
    problem_group_ids = permissions.values_list('problem_group', flat=True)
    problem_groups = ProblemGroup.objects.filter(id__in=problem_group_ids)

    problems = QuerySet()
    for problem_group in problem_groups:
        problems.union(problem_group.problems.all())
    return problems


def _problems_to_list(user, problems):
    result = []
    for problem in problems:
        all_record = Record.objects.filter(problem=problem)
        all_right_record = all_record.filter(result=True)
        user_record = all_record.filter(user=user)
        user_right_record = user_record.filter(result=True)
        result.append({
            'title': problem.title,
            # 需要同时返回 problem_group_creator，problem_group_title，index
            # 因为 problem_group_creator 和 problem_group_title 唯一确定一个题单（问题组）
            # 问题组和 index 唯一确定一个问题
            'problem_group_creator': problem.problem_group.user.username,
            'problem_group_title': problem.problem_group.title,
            'index': problem.index,
            'tags': [tag.name for tag in problem.tags.all()],
            'creator': problem.creator.username,
            # 用于展示用户是否做过此题（user_count）并计算个人正确率、总正确率
            'user_right_count': user_right_record.count(),
            'user_count': user_record.count(),
            'all_right_count': all_right_record.count(),
            'all_count': all_record.count(),
        })
    return result


@require_http_methods(["POST"])
def get_problem_num_with_permissions(request):
    username = request.POST.get('username')
    user = User.objects.get(username=username)
    if not user:
        return E_USER_NOT_FIND
    user = user[0]

    problems = _get_problems_with_permissions(user)
    return success_data("问题数量查询成功", problems.count())


@require_http_methods(["POST"])
def get_problems_with_permissions(request):
    username = request.POST.get('username')
    user = User.objects.get(username=username)
    if not user:
        return E_USER_NOT_FIND
    user = user[0]

    problems = _get_problems_with_permissions(user)
    if not problems:
        return E_NO_PROBLEM

    problems = _cut_to_page(request, problems, sort_key, reverse)

    return success_data("问题查询成功", _problems_to_list(user, problems))


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
    return success(result)


data = [
    {
        "id": 1,
        "problem_title": "如何计算矩阵的行列式？",
        "problem_group_title": "Math Questions",
        "problem_group_id": 101,
        "tags": ["矩阵", "行列式"],
        "creator": "user123",
        "user_right_count": 5,
        "user_count": 10,
        "all_right_count": 150,
        "all_count": 300,
    },
    {
        "id": 2,
        "problem_title": "求解线性方程组的解",
        "problem_group_title": "Math Questions",
        "problem_group_id": 101,
        "tags": ["线性代数", "方程组"],
        "creator": "user456",
        "user_right_count": 3,
        "user_count": 8,
        "all_right_count": 200,
        "all_count": 400,
    },
]


# 视图函数
@require_http_methods(["POST"])
def get_problems_fake(request):
    # 构建成功响应的数据结构
    response_data = {
        "code": 200,
        "message": "问题查询成功",
        "data": data
    }
    return JsonResponse(response_data, safe=False)  # 使用safe=False允许返回非字典类型的数据
