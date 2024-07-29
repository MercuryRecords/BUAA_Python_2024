from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import User


def edit_avatar(request):
    username = request.POST.get('username')
    avatar = request.FILES.get('avatar')

    user = User.objects.get(username=username)
    if not user:
        res = {'code': 401, 'message': '用户不存在'}
        return JsonResponse(res)

    if user.avatar:
        user.avatar.delete()
    user.avatar = avatar
    user.save()

    res = {'code': 200, 'message': '头像修改成功'}
    return JsonResponse(res)



@require_http_methods(["POST"])
def get_avatar(request):  # 获取用户头像
    username = request.POST.get('username')
    user = User.objects.get(username=username)
    if not user:
        res = {'code': 401, 'message': '用户不存在'}
        return JsonResponse(res)

    if user.avatar:
        res = {'code': 200, 'message': '头像获取成功', 'avatar': user.avatar.url}
    else:
        res = {'code': 200, 'message': '头像获取成功', 'avatar': 'default.png'}

    return JsonResponse(res)

