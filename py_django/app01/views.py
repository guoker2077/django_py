from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages

# 在视图中使用 LoginForm 和 RegisterForm


# Create your views here.
def index(request):
    return render(request,"index.html")

def user_list(request):
    return render(request,"user_list.html")

def user_add(request):
    if request.method == 'POST':
        print("is in post")
        if request.POST.get('action') == 'login':
            print("is in login")
            form = LoginForm(request.POST)
            if form.is_valid():
                print("is in valid")
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    print("登录成功")
                    login(request, user)
                    return redirect('../index/')  # 登录成功跳转
                else:
                    # 登录失败逻辑
                    print("登录失败")
                    messages.error(request, '登录失败，用户名或密码不正确')
                    return redirect('user_add')

        elif request.POST.get('action') == 'register':
            form = RegisterForm(request.POST)
            if form.is_valid():
                # 创建用户逻辑
                User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    # 其他字段...
                )
                return redirect('user/index/')
            else:
                # 注册失败逻辑
                messages.error(request, '表单数据无效，请重新输入')

    else:
        print("is in get")

    return render(request, 'user_add.html', {
        'login_form': form if 'login' in request.POST else LoginForm(),
        'register_form': form if 'register' in request.POST else RegisterForm(),
    })


def user_edit(req):
    name = 'zjp'
    import requests
    url = "https://jsonplaceholder.typicode.com/users"
    res = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    data_list = res.json()
    return render(req,"user_edit.html",{"n1":name,"data_list":data_list})