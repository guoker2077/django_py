from django.shortcuts import render, HttpResponse,redirect


# Create your views here.
def index(request):
    return HttpResponse("欢迎使用！ ")


def user_list(request):
    # 1，优先去项目根目录的templates中寻找 （配置了的顺序）
    # 2．根据app的注册顺序，在每个app下的templates目录中寻找（我们的）
    return render(request, 'user_list.html')


def user_add(request):
    names = "张俊杰"
    roles = ['管理员', 'CEO', '保安']
    return render(request, 'user_add.html')


def stu_gramma(request):
    names = "张俊杰"
    roles = ['管理员', 'CEO', '保安']
    user_info = {"name": "zjj", 'salary': 1000, 'role': 'CEO'}
    name_list = [
        {"name": "zjj", 'salary': 1000, 'role': 'CEO'},
        {"name": "zxx", 'salary': 2000, 'role': 'CTO'},
        {"name": "zxj", 'salary': 1600, 'role': 'CFO'}, ]
    return render(request, 'stu_gramma.html', {'n1': names, 'n2': roles, 'n3': user_info, 'n4': name_list})


def news(request):
    # 构造新闻（字典，列表）
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    # res = requests.get('https://adx.36kr.com/api/ad/show?param.positionIds=811', headers=headers)
    # data_list = res.json()
    data_list = {'code': 0, 'data': {'adList': [{'positionId': 817, 'requestId': '5712e35ff1174fb0a60ffbff047c6bd5', 'planId': 19212, 'planType': 1, 'adSdk': 'jCEeQPwq9UMo-XNwK35KQkdlYFNPpYXva2nkkDWdagBerefdpbA6zn9iJ0x7w-6FpWtws9TG6E85Af0DeW5BIw', 'adExposureUrl': 'https://adx.36kr.com/api/ad/exposure?sign=720c45e53d8a40913353a8d028b7cb30&param.adsdk=jCEeQPwq9UMo-XNwK35KQkdlYFNPpYXva2nkkDWdagBerefdpbA6zn9iJ0x7w-6FpWtws9TG6E85Af0DeW5BIw', 'adJsonContent': '{"src":"https://img.36krcdn.com/hsossms/20231025/v2_a4085f35c363441a82dc027be235f92c@000000_oswg45637oswg1380oswg280_img_jpg","href":"https://adx.36kr.com/api/ad/click?sign=1c48c7f1bf91bfb56773b95f09160606&param.redirectUrl=aHR0cHM6Ly81OTIxNDA0NDg4ODExLmh1b2Rvbmd4aW5nLmNvbS9ldmVudC80NzI1Njk5NDk3NTAw&param.adsdk=jCEeQPwq9UMo-XNwK35KQkdlYFNPpYXva2nkkDWdagBerefdpbA6zn9iJ0x7w-6FpWtws9TG6E85Af0DeW5BIw"}', 'flag': '商业策划', 'startTime': 1700150400000, 'endTime': 1700236799999}]}}
    # print(data_list)
    return render(request, 'news.html', {'data_list':data_list})

def req(request):
    # request 是一个对象，封装了用户发过来的所有数据

    # 1. 获取请求方式 GET/POST
    print(request.method)

    # 2. 在URL上传递值  /req/?n1=123&n2=456
    print(request.GET) # <QueryDict: {'n1': ['123'], 'n2': ['456']}>

    # 3. 在请求体中提交数据
    print(request.POST)

    # 4. [响应] HttpResponse("返回数据")，内容字符串返回给请求者
    # return HttpResponse("返回数据")

    # 5. [响应] 读取HTML内容 + 渲染（替换）+ 内容字符串返回给请求者
    # return render(request,'req.html',{'title':"来了"})

    # 6. [响应] 重定向
    return redirect('https://www.google.com')


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:

        # print(request.POST)
        post = request.POST
        username = post.get("user")
        password = post.get("password")

        if username == 'root' and password == '123':
            # return HttpResponse("登录成功！")
            # 进入登录页面
            return redirect('https://www.lzu.edu.cn')
        else:
            return render(request,'login.html',{'err_msg':"登录失败！"})