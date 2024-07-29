from django.views.decorators.http import require_http_methods
from .errors import *

from .models import Record, User, TemporaryProblemGroup
from .views_problem import _problem_to_dict, _cut_to_page


@require_http_methods(["POST"])
def get_records_num(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)

    if not user:
        return E_USER_NOT_FIND

    user = user[0]
    records = Record.objects.filter(user=user, result=False)
    # 得到所有题目的集合
    problems = set(record.problem for record in records)

    return success_data("错题数量获取成功", data=len(problems))


@require_http_methods(["POST"])
# 获取与用户有关的所有错题
def get_records(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return E_USER_NOT_FIND

    user = user[0]
    records = Record.objects.filter(user=user, result=False)
    # 得到所有题目的集合
    problems = set(record.problem for record in records)

    if not problems:
        return E_NO_PROBLEM_GROUP

    rate = dict()
    for problem in problems:
        rate[problem] = sum(1 for record in records if record.problem == problem) / len(
            Record.objects.filter(user=user, problem=problem))

    methods = request.POST.get('methods')
    if not methods:
        problems = sorted(problems, key=lambda x: max(record.created_at for record in records if record.problem == x),
                          reverse=True)
    # LRU
    elif methods == 'lru':
        problems = sorted(problems, key=lambda x: max(record.created_at for record in records if record.problem == x))
    # 错误率降序
    elif methods == 'error_rate':
        problems = sorted(problems, key=lambda x: rate[x], reverse=True)
    # 错误率升序
    elif methods == 'error_rate_rev':
        problems = sorted(problems, key=lambda x: rate[x])
    else:
        problems = sorted(problems, key=lambda x: max(record.created_at for record in records if record.problem == x),
                          reverse=True)

    problems = _cut_to_page(request, problems)
    if isinstance(problems, JsonResponse):
        return problems

    lst = []

    for problem in problems:
        dct = _problem_to_dict(user, problem)
        dct['last_error_time'] = max(record.created_at for record in records if record.problem == problem)
        lst.append(dct)

    return success_data("错题获取成功", lst)
