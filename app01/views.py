from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

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
from .forms import ProfileForm
from .models import UserInfo
import subprocess
from app01.image_recognition.ResNet50 import recognize_image


# 在视图中使用 LoginForm 和 RegisterForm


# Create your views here.

@csrf_exempt  # 如果使用 AJAX 且跨域，可能需要此装饰器
def user_add(request):
    if request.method == 'POST':
        print("is in post")
        # 检查请求体是否非空
        # 打印请求头和请求体的内容，用于调试
        print("Request Headers:", request.headers)
        print("Request Body:", request.body)
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

        if action == 'username_login':
            username = data.get('username')
            password = data.get('password')
            print("username and password", username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_url = reverse('user_home_alreadyin', kwargs={'user_id': user.id})
                return JsonResponse({'message': redirect_url})
            else:
                return JsonResponse({'error': '登录失败，用户名或密码不正确'}, status=400)

        elif action == 'phone_login':
            phone = data.get('phone')
            input_code = data.get('code')
            print("phone and code", phone, input_code)
            # 验证码验证逻辑
            correct_code = cache.get(phone)
            if correct_code is None or str(correct_code) != input_code:
                return JsonResponse({'error': '验证码错误'}, status=400)

            # 手机号用户查找逻辑
            try:
                user_info = UserInfo.objects.get(phone=phone)
                user = user_info.user
                login(request, user)
                redirect_url = reverse('user_home_alreadyin', kwargs={'user_id': user.id})
                return JsonResponse({'message': redirect_url})
            except UserInfo.DoesNotExist:
                return JsonResponse({'error': '未找到用户'}, status=404)

        elif action == 'register':
            print("is in register")

            print("is in valid")
            # 从 JSON 数据中提取注册信息
            username = data.get('username')
            password = data.get('password')
            phone = data.get('phone')
            input_code = data.get('code')

            # 从缓存中获取正确的验证码

            correct_code = cache.get(phone)
            print("phone is ", phone)
            print("input_code is ", input_code)
            print("username is ", username)
            print("password is ", password)
            print("correct_code is ", correct_code)
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
            redirect_url = '/user/add'
            return JsonResponse({'message': redirect_url})

        elif action == 'send_code_login':
            print("send code login")
            phone_number = data.get('phone')

            # 检查手机号是否已注册
            if not UserInfo.objects.filter(phone=phone_number).exists():
                print("您的手机号未注册")
                return JsonResponse({'error': '您的手机号未注册'}, status=200)
            print("您的手机号已注册")

            # 检查是否已发送过验证码且在10分钟内
            last_sent_time = cache.get(f"{phone_number}_sent_time")
            if last_sent_time and datetime.now() - last_sent_time < timedelta(minutes=10):
                return JsonResponse({'error': '验证码发送过于频繁'}, status=200)

            code = random.randint(100000, 999999)
            cache.set(phone_number, code, 600)  # 保存验证码10分钟
            # TODO: 实际发送验证码逻辑（调用短信API）
            print(f"验证码 {code} 已发送到 {phone_number}")

            return JsonResponse({'message': '验证码已发送'})

        elif action == 'send_code_reg':
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


@csrf_exempt  # 如果使用 AJAX 且跨域，可能需要此装饰器
def user_info(request, user_id):
    # 确保当前有用户登录
    if user_id is None:
        # 重定向到登录页面或显示错误信息
        return redirect('user_add')
    user_data = UserInfo.objects.filter(user_id=user_id).first()
    if user_data is not None:
        data_username = user_data.user
        data_name = user_data.name
        data_avatar = user_data.avatar
        data_phone = user_data.phone
        data_gender = user_data.gender
        data_age = user_data.age
        data_balance = user_data.balance

    # 检查用户是否有关联的 UserInfo 实例
    userinfo, created = UserInfo.objects.get_or_create(user=request.user)

    action = request.POST.get('action')
    print(action)
    form = ProfileForm(request.POST, request.FILES, instance=userinfo)
    if form.is_valid():
        form.save()
        # 处理其他逻辑...
        info_url = reverse('user_info', args=(user_id,))
        return redirect(info_url)  # 使用reverse获取带有用户ID的URL并重定向
    elif action == 'send_code1':
        print("send code1")
        phone_number = request.POST.get('phone')
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        userinfo = UserInfo.objects.get(user=user)
        if phone_number != userinfo.phone:
            print("手机号错误")
            return JsonResponse({'error': '手机号错误'}, status=200)
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
    elif action == 'send_code2':
        print("send code2")
        phone_number = request.POST.get('phone')
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        userinfo = UserInfo.objects.get(user=user)
        if phone_number != userinfo.phone:
            print("手机号错误")
            return JsonResponse({'error': '手机号错误'}, status=200)
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
    elif action == 'profile':
        print("profile")
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        user_id = request.POST.get('user_id')
        avatar = request.FILES.get('avatar')
        avatar_url = None
        if avatar:
            fs = FileSystemStorage()
            filename = fs.save(avatar.name, avatar)
            avatar_url = fs.url(filename)

        user = User.objects.get(id=user_id)
        user.username = username
        user.save()
        userinfo = UserInfo.objects.get(user=user)
        userinfo.name = nickname
        userinfo.age = age
        userinfo.gender = gender
        if avatar_url:
            userinfo.avatar = avatar_url
        userinfo.save()
        redirect_url = reverse('user_info', kwargs={'user_id': user.id})
        return JsonResponse({'message': redirect_url})
    elif action == 'verifyPhoneModal1-form':
        print("is in verifyPhoneModal1-form")

        print("is in valid")
        # 从 JSON 数据中提取注册信息
        phone = request.POST.get('phone')
        input_code = request.POST.get('code')
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        userinfo = UserInfo.objects.get(user=user)
        print(phone)
        print(userinfo.phone)
        # 从缓存中获取正确的验证码
        correct_code = cache.get(phone)
        print("phone is ", phone)
        print("input_code is ", input_code)
        print("correct_code is ", correct_code)
        # 检查验证码是否正确
        print("has sent code")
        if correct_code is None or str(correct_code) != input_code:
            print("验证码错误")
            return JsonResponse({'error': '验证码错误'}, status=400)
        print("验证码正确")
        return JsonResponse({'message': '注册成功'})
    elif action == 'verifyPhoneModal2-form':
        print("is in verifyPhoneModal2-form")

        print("is in valid")
        # 从 JSON 数据中提取注册信息
        phone = request.POST.get('phone')
        input_code = request.POST.get('code')
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        userinfo = UserInfo.objects.get(user=user)
        print(phone)
        print(userinfo.phone)
        # 从缓存中获取正确的验证码
        correct_code = cache.get(phone)
        print("phone is ", phone)
        print("input_code is ", input_code)
        print("correct_code is ", correct_code)
        # 检查验证码是否正确
        print("has sent code")
        if correct_code is None or str(correct_code) != input_code:
            print("验证码错误")
            return JsonResponse({'error': '验证码错误'}, status=400)
        print("验证码正确")
        return JsonResponse({'message': '注册成功'})
    elif action == 'newPasswordModal-form':
        print("is in newPasswordModal-form")

        print("is in valid")
        # 从 JSON 数据中提取注册信息
        new_password = request.POST.get('new-password')
        print(new_password)
        user_id = request.POST.get('user_id')
        print(user_id)
        user = User.objects.get(id=user_id)
        userinfo = UserInfo.objects.get(user=user)
        user.set_password(new_password)
        user.save()
        userinfo.save()
        print("nb")
        return JsonResponse({'message': '修改成功'})
    elif action == 'changePhoneModal-form':
        print("is in changePhoneModal-form")

        print("is in valid")
        # 从 JSON 数据中提取注册信息
        new_phone = request.POST.get('new-phone')
        print(new_phone)
        user_id = request.POST.get('user_id')
        print(user_id)
        user = User.objects.get(id=user_id)
        userinfo = UserInfo.objects.get(user=user)
        userinfo.phone = new_phone
        user.save()
        userinfo.save()
        print("nb")
        return JsonResponse({'message': '修改成功'})



    else:
        form = ProfileForm(instance=userinfo)

    return render(request, 'user_info.html',
                  {'form': form, "data_username": data_username, "data_name": data_name, "data_avatar": data_avatar,
                   "data_phone": data_phone, "data_gender": data_gender, "data_age": data_age,
                   "data_balance": data_balance, "user_id": user_id})


def user_home_alreadyin(request, user_id):
    user_data = UserInfo.objects.filter(user_id=user_id).first()
    user_name = user_data.name
    user_balance = user_data.balance
    user_avatar = user_data.avatar
    return render(request, 'home_page_alreadyin.html',
                  {"user_id": user_id, "user_name": user_name, "user_balance": user_balance,
                   "user_avatar": user_avatar})


def user_home(req):
    return render(req, 'Home_page.html')


@csrf_exempt  # 如果使用 AJAX 且跨域，可能需要此装饰器
def user_func_image_strengthen(request, user_id):
    if user_id:
        user_data = UserInfo.objects.filter(user_id=user_id).first()
        user_name = user_data.name
        user_balance = user_data.balance
        user_avatar = user_data.avatar
    if request.method == 'POST':
        action = request.POST.get('action')
        print(action)
        if action == 'profile':
            user = User.objects.get(id=user_id)
            userinfo = UserInfo.objects.get(user=user)
            if user_balance >= 1:
                user_balance -= 1
                userinfo.balance = user_balance
                user.save()
                userinfo.save()
            else:
                return JsonResponse({'error': '余额不足'}, status=201)
            avatar = request.FILES.get('avatar')
            if avatar:
                fs = FileSystemStorage()
                filename = fs.save(avatar.name, avatar)
                exe_path = './app01/realesrgan-ncnn-vulkan-20220424-windows/realesrgan-ncnn-vulkan.exe'
                input_image = './app01/static/img/' + avatar.name
                output_image = './app01/static/img/output_' + avatar.name
                model_name = 'realesrgan-x4plus'
                command = [exe_path, '-i', input_image, '-o', output_image, '-n', model_name]
                subprocess.run(command, check=True)
                output_image_url = '/static/img/output_' + avatar.name
                return JsonResponse({'message': output_image_url})

    return render(request, "user_func_image_strengthen.html",{"user_id": user_id, "user_name": user_name, "user_balance": user_balance,
                   "user_avatar": user_avatar})


@csrf_exempt  # 如果使用 AJAX 且跨域，可能需要此装饰器
def user_func_image_recognition(request, user_id):
    if user_id:
        user_data = UserInfo.objects.filter(user_id=user_id).first()
        user_name = user_data.name
        user_balance = user_data.balance
        user_avatar = user_data.avatar
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'profile':
            user = User.objects.get(id=user_id)
            userinfo = UserInfo.objects.get(user=user)
            if user_balance >= 1:
                user_balance -= 1
                userinfo.balance = user_balance
                user.save()
                userinfo.save()
            else:
                return JsonResponse({'error': '余额不足'}, status=201)
            image = request.FILES.get('avatar')
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                filename2 = "app01/static/img/" + filename
                results = recognize_image(filename2)

                fs.delete(filename)
                # 返回 JSON 数据
                return JsonResponse({'results': results})

    return render(request, "user_func_image_recognition.html",{"user_id": user_id, "user_name": user_name, "user_balance": user_balance,
                   "user_avatar": user_avatar})


@csrf_exempt  # 如果使用 AJAX 且跨域，可能需要此装饰器
def admin_login(request):
    if request.method == 'POST':
        print("is in post")
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("username and password", username, password)
        # 检查请求体是否非空
        # 打印请求头和请求体的内容，用于调试
        # print("Request Headers:", request.headers)
        # print("Request Body:", request.body)
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
        # username = data.get('username')
        # print(username)
        if action == 'admin_login':
            username = data.get('username')
            password = data.get('password')
            print("username and password", username, password)

            if username == 'admin' and password == '123456':
                admin = authenticate(username=username, password=password)
                login(request, admin)
                redirect_url = reverse('admin_main')
                return JsonResponse({'message': redirect_url})
            else:
                return JsonResponse({'error': '登录失败，用户名或密码不正确'}, status=400)

    return render(request, 'admin_login.html')


@csrf_exempt  # 如果使用 AJAX 且跨域，可能需要此装饰器
def admin_main(request):
    admin = request.user
    user_infos = UserInfo.objects.all()

    context = {
        'admin': admin,
        'user_infos': user_infos
    }

    return render(request, 'admin_main.html', context)
