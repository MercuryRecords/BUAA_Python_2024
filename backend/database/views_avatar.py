import os
import hashlib
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .models import User


def generate_encrypted_filename(username):
    timestamp = timezone.now().timestamp()
    filename = f"{username}_{timestamp}"
    encrypted_filename = hashlib.md5(filename.encode('utf-8')).hexdigest()
    return encrypted_filename


@require_http_methods(["POST"])
def edit_avatar(request):
    username = request.POST.get('username')
    user = User.objects.get(username=username)
    if not user:
        res = {'code': 401, 'message': '用户不存在'}
        return JsonResponse(res)

    avatar = request.FILES.get('avatar')
    file_extension = os.path.splitext(avatar.name)[1]
    new_filename = generate_encrypted_filename(username) + file_extension

    if user.avatar and user.avatar.name != 'avatars/default.png':
        user.avatar.delete()
    user.avatar.save(new_filename, avatar)
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

    res = {'code': 200, 'message': '头像获取成功', 'avatar': request.build_absolute_uri(user.avatar.url)}

    return JsonResponse(res)
