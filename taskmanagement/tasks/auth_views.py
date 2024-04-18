from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # 修改為註冊成功後要跳轉的頁面，比如首頁
    else:
        form = UserCreationForm()
    # return HttpResponse("Event創建失敗。")
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/tasks')  # 修改為登錄成功後要跳轉的頁面，比如首頁
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/login')  # 修改為登出後要跳轉的頁面，比如首頁

def task_view(request):
    username = request.user.username  # 獲取當前登錄用戶的用戶名
    return render(request, 'create_event.html', {'username': username})

# @login_required  # 添加登录验证装饰器，确保只有登录用户才能访问该视图
def my_view(request):
    if request.user.is_authenticated:  # 检查用户是否已经登录
        # 用户已登录，可以执行相应的操作，如获取用户名
        username = request.user.username
        return render(request, 'create_event.html', {'username': username})
    else:
        # 用户未登录，可以返回未登录提示或者重定向到登录页面
        return HttpResponse("請先登錄")