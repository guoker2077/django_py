from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.cache import cache
import random
from datetime import datetime, timedelta
from app01.models import UserInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json



# 在视图中使用 LoginForm 和 RegisterForm


# Create your views here.
def index(request):
    return render(request,"index.html")

def user_list(request):
    return render(request,"user_list.html")


@csrf_exempt  # 如果使用 AJAX 且跨域，可能需要此装饰器
def user_add(request):

    if request.method == 'POST':
        print("is in post")
        # 检查请求体是否非空
        if request.body:
            try:
                data = json.loads(request.body)
                action = data.get('action')

            except json.JSONDecodeError:
                # 如果不是有效的 JSON，可能是普通的表单请求
                # 在这里处理表单逻辑
                print("is in json.JSONDecodeError")
                action = request.POST.get('action')
        else:
            # 如果请求体为空，处理为普通表单请求
            action = request.POST.get('action')

        if action == 'login':
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


        elif action == 'register':
            print("is in register")
            form = RegisterForm(request.POST)


            print("is in valid")
            # 从 JSON 数据中提取注册信息
            username = data.get('username')
            password = data.get('password')
            phone = data.get('phone')
            input_code = data.get('code')

            # 从缓存中获取正确的验证码

            correct_code = cache.get(phone)
            print("phone is ",phone)
            print("input_code is ",input_code)
            print("username is ",username)
            print("password is ",password)
            print("correct_code is ",correct_code)
            # 检查验证码是否正确
            print("has sent code")
            if correct_code is None or str(correct_code) != input_code:
                print("验证码错误")
                return JsonResponse({'error': '验证码错误'}, status=400)
            print("验证码正确")
            # 创建用户逻辑

            # 创建auth_user记录
            user = User.objects.create_user(username=username, password=password)

            # 创建app01_userinfo记录
            userinfo = UserInfo(user=user, phone=phone)
            # 您可以在此添加任何其他字段，例如：userinfo.name = 'Your Name'
            userinfo.save()

            return JsonResponse({'message': '注册成功'})




        elif action == 'send_code':
            print("send code")
            phone_number = data.get('phone')

            # 检查是否已发送过验证码且在10分钟内
            last_sent_time = cache.get(f"{phone_number}_sent_time")
            if last_sent_time and datetime.now() - last_sent_time < timedelta(minutes=10):
                return JsonResponse({'error': '验证码发送过于频繁'}, status=429)

            code = random.randint(100000, 999999)
            cache.set(phone_number, code, 600)  # 保存验证码10分钟
            cache.set(f"{phone_number}_sent_time", datetime.now(), 600)  # 保存发送时间10分钟

            # TODO: 实际发送验证码逻辑（调用短信API）
            print(f"验证码 {code} 已发送到 {phone_number}")

            return JsonResponse({'message': '验证码已发送'})


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