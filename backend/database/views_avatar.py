import os
import hashlib

from django.core.files.storage import FileSystemStorage
from django.conf import settings
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
    # file_extension = os.path.splitext(avatar.name)[1]
    # print(f"f_ext: {file_extension}")
    # new_filename = generate_encrypted_filename(username) + file_extension
    # file_path = os.path.join('avatars', new_filename)
    # avatar_file_path = user.avatar.save(file_path, avatar)
    # print(f"avatar_file_path: {avatar_file_path}")

    print(user.avatar.name)
    if user.avatar and user.avatar.name != 'avatars/default.png':
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

    print(user.avatar.name)

    res = {'code': 200, 'message': '头像获取成功', 'avatar': request.build_absolute_uri(user.avatar.url)}

    return JsonResponse(res)
