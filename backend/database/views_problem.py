from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from .models import User, ProblemGroup, Problem, ProblemPremission

@require_http_methods(["POST"])
def problem_group_create(request):
    username = request.POST.get('username')
    title = request.POST.get('title')
    description = request.POST.get('description')

    check = User.objects.filter(username=username)
    if not check:
        return JsonResponse({"code": 401, "message": "用户不存在"})

    if len(title) > 50:
        return JsonResponse({"code": 402, "message": "标题长度不能超过50"})

    if len(description) > 200:
        return JsonResponse({"code": 403, "message": "描述长度不能超过200"})
    
    if ProblemGroup.objects.filter(user=check[0], title=title):
        return JsonResponse({"code": 404, "message": "问题组已存在"})

    ProblemGroup.objects.create(user=check[0], title=title, description=description)
    return JsonResponse({"code": 200, "message": "问题组创建成功"})

@require_http_methods(["POST"])
def problem_create(request):
    username = request.POST.get('username')
    problem_group_title = request.POST.get('problem_group_title')
    type = request.POST.get('type')
    content = request.POST.get('content')
    ans_count = request.POST.get('ans_count')
    answer = request.POST.get('answer')
    field1 = request.POST.get('field1')
    field2 = request.POST.get('field2')
    field3 = request.POST.get('field3')
    field4 = request.POST.get('field4')
    field5 = request.POST.get('field5')
    field6 = request.POST.get('field6')
    field7 = request.POST.get('field7')