from django.shortcuts import render
from models import User


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(username=username)
        if users:
            # 用户名已经存在，不予注册，返回错误信息
            return render(request, 'register.html', {'error_message': '用户名已存在。'})
            pass
        else:
            # 创建用户并加入到数据库中，返回注册成功信息
            User.objects.create_user(username=username, password=password)

    return render(request, 'register.html')


def user_login(request):
    pass