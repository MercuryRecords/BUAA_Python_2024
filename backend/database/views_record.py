from django.views.decorators.http import require_http_methods
from .error import *

from .models import Record, User
from .views_problem import _problems_to_dict, _cut_to_page


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
        return E_PROBLEM_NOT_FIND

    problems = _cut_to_page(request, problems)
    if isinstance(problems, JsonResponse):
        return problems

    methods = request.POST.get('methods')
    if not methods:
        problems = sorted(problems, key=lambda x: max(record.created_at for record in records if record.problem == x), reverse=True)
    # LRU
    elif methods == 'lru':
        problems = sorted(problems, key=lambda x: max(record.created_at for record in records if record.problem == x))

    else:
        problems = sorted(problems, key=lambda x: max(record.created_at for record in records if record.problem == x), reverse=True)

    return success_data("错题获取成功", data=_problems_to_dict(problems))
