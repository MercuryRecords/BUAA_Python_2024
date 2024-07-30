from django.views.decorators.http import require_http_methods

from .models import User, Tag, Problem, Record
from .errors import *

import time

percent = [10, 8, 4, 2, 1]

def calc_single_problem_master_rate(records_from):
    records = records_from.order_by('-created_at')
    limit = min(len(percent), records.count())
    rate_u = 0
    rate_d = 0
    for i in range(limit):
        record = records[i]
        if record.result:
            rate_u += percent[i]
        rate_d += percent[i]
    return rate_u / rate_d if rate_d else 0.0


def _update_dict(dict, problem_id, is_correct):
    if not problem_id in dict:
        dict[problem_id] = [0, 0]
    
    data = dict[problem_id]
    count = data[1]
    if count >= len(percent):
        return
    
    if is_correct:
        data[0] += percent[count]
    data[1] = count + 1

def _calc_difficulty(problem_id):
    problem = Problem.objects.get(id=problem_id)
    all_record = Record.objects.filter(problem=problem)
    all_right_record = all_record.filter(result=True)
    return 10 - all_right_record.count() * 9 / all_record.count() if all_record else 1

def _calc_ability(dict):
    ability = 0.0
    for key, value in dict.items():
        difficulty = _calc_difficulty(key)
        base = 0
        for i in range(value[1]):
            base += percent[i]
        ability += difficulty * value[0] / base # value[0] / base 是题目掌握度
    return ability

# @require_http_methods(["POST"])
# def get_ability_trace(request):
#     user = User.objects.get(username=request.POST.get('username'))
#     during_interval = int(request.POST.get('during_interval'))
#     during_num = int(request.POST.get('during_num'))
#     filter_tag = request.POST.get('filter_tag')
#     current_time = (int(time.time()) + 28800) // during_interval # 28800为8个小时的秒数

#     if filter_tag:
#         tag = Tag.objects.filter(name=filter_tag)
#         if not tag:
#             return E_TAG_NOT_FIND
#         problems = tag[0].problems.all()
#         problems = problems.exclude(creator=user)
#     else:
#         problems = Problem.objects.exclude(creator=user)
    
#     records = Record.objects.filter(user=user, problem__in=problems).order_by('-created_at')
#     # 伟大的列表套字典套列表
#     datas = [{} for _ in range(during_num)]
#     for record in records:
#         record_time = (record.get_unix_timestamp() + 28800) // during_interval
#         update_limit = min(current_time - record_time + 1, during_num)
#         for i in range(0, update_limit):
#             _update_dict(datas[i], record.problem.id, record.result)
    
#     result = []
#     for data in datas:
#         result.append(_calc_ability(data))

#     return success_data("能力值获取成功", result[::-1])

@require_http_methods(["POST"])
def get_ability_trace(request):
    user = User.objects.get(username=request.POST.get('username'))
    during_interval = int(request.POST.get('during_interval'))
    during_num = int(request.POST.get('during_num'))
    filter_tag = request.POST.get('filter_tag')
    current_time = int(time.time())

    if filter_tag:
        tag = Tag.objects.filter(name=filter_tag)
        if not tag:
            return E_TAG_NOT_FIND
        problems = tag[0].problems.all()
        problems = problems.exclude(creator=user)
    else:
        problems = Problem.objects.exclude(creator=user)
    
    records = Record.objects.filter(user=user, problem__in=problems).order_by('-created_at')
    # 伟大的列表套字典套列表
    datas = [{} for _ in range(during_num)]
    for record in records:
        record_time = (current_time - record.get_unix_timestamp()) // during_interval
        update_limit = min(record_time + 1, during_num)
        for i in range(0, update_limit):
            _update_dict(datas[i], record.problem.id, record.result)
    
    result = []
    for data in datas:
        result.append(_calc_ability(data))

    return success_data("能力值获取成功", result[::-1])

@require_http_methods(["POST"])
def get_advantaged_tags(request):
    user = User.objects.get(username=request.POST.get('username'))
    num = request.POST.get('required_num')

    problems = Problem.objects.exclude(creator=user)
    records = Record.objects.filter(user=user, problem__in=problems).order_by('-created_at')
    # 伟大的字典套字典套列表
    data = {}
    for record in records:
        for tag in record.problem.tags.all():
            if tag.name in ['选择题', '填空题']:
                continue
            if tag.name not in data:
                data[tag.name] = {}
            _update_dict(data[tag.name], record.problem.id, record.result)

    result = []
    for key, value in data.items():
        result.append([key, _calc_ability(value)])
    
    result.sort(key=lambda x: x[1], reverse=True)
    if num:
        result = result[:int(num)]
    result = [{'name': item[0], 'ability_value': item[1]} for item in result]

    return success_data("获取优势标签成功", result)

def _calc_correct_rate(problem_id):
    problem = Problem.objects.get(id=problem_id)
    all_record = Record.objects.filter(problem=problem)
    all_right_record = all_record.filter(result=True)
    return all_right_record.count() / all_record.count() if all_record else 0.0

def _calc_weakness(dict):
    weakness_u = 0.0
    weakness_d = 0.0
    for key, value in dict.items():
        correct_rate = _calc_correct_rate(key)
        base = 0
        for i in range(value[1]):
            base += percent[i]
        weakness_u += correct_rate - correct_rate * value[0] / base # value[0] / base 是题目掌握度
        weakness_d += correct_rate
    return weakness_u / weakness_d if weakness_d else 0.0


@require_http_methods(["POST"])
def get_disadvantaged_tags(request):
    user = User.objects.get(username=request.POST.get('username'))
    num = request.POST.get('required_num')

    problems = Problem.objects.exclude(creator=user)
    records = Record.objects.filter(user=user, problem__in=problems).order_by('-created_at')
    # 伟大的字典套字典套列表
    data = {}
    for record in records:
        for tag in record.problem.tags.all():
            if tag.name in ['选择题', '填空题']:
                continue
            if tag.name not in data:
                data[tag.name] = {}
            _update_dict(data[tag.name], record.problem.id, record.result)
    
    result = []
    for key, value in data.items():
        result.append([key, _calc_weakness(value)])
    result.sort(key=lambda x: x[1], reverse=True)
    if num:
        result = result[:int(num)]
    result = [{'name': item[0], 'weakness_value': item[1]} for item in result]

    return success_data("获取劣势标签成功", result)
