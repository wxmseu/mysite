from django.shortcuts import render, redirect, HttpResponse
from myblog.utils.form import LoginForm, RegisterModelForm
from myblog import models
from myblog.utils.code import check_code
from io import BytesIO
from datetime import datetime, timedelta
from myblog.utils.encrypt import md5
from myblog.utils.send_email import send_email
from django.conf import settings


# Create your views here.
def homepage(request):
    return render(request, 'myblog/homepage.html')


def login(request):
    """用户登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'myblog/login.html', {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 校验验证码

        code = form.cleaned_data.pop('code')
        req_code = request.session.get('code_string', '')
        if code.upper() != req_code.upper():
            form.add_error("code", '验证码错误')
            return render(request, 'myblog/login.html', {"form": form})
        # 校验成功，获得用户输入的用户名和密码，从数据库中去比对
        user_data = models.AdminInfo.objects.filter(**form.cleaned_data).first()
        if not user_data:
            # 如果输入错误，弹出提示信息
            form.add_error("password", "输入的用户名或者密码错误 ")
            return render(request, 'myblog/login.html', {"form": form})
        # 校验邮箱是否确认
        if user_data.has_confirmed == 0:
            form.add_error('password', '您的注册邮箱未确认，请前往邮箱确认后重新登录')
            return render(request, 'myblog/login.html', {"form": form})
        # 信息输入正确
        # 网站随机生成字符串，写到用户浏览器的cookies，再写到session中
        request.session["info"] = {"id": user_data.id, "username": user_data.username}
        # 设置session维持时间3天
        request.session.set_expiry(60 * 60 * 24 * 3)
        return redirect('/')
    return render(request, 'myblog/login.html', {"form": form})


def make_code_string(username):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = md5(username) + md5(now)
    return code


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'myblog/register.html', {"form": form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        code = form.cleaned_data.pop('code')
        session_code = request.session.get('code_string', '')
        if code.upper() != session_code.upper():
            form.add_error("code", '验证码错误')
            return render(request, 'myblog/register.html', {"form": form})
        form.save()

        email_code = make_code_string(form.cleaned_data.get('username'))
        send_email(form.cleaned_data.get('email'), email_code)
        models.ConfirmUserEmail.objects.create(user=form.cleaned_data.get('username'), code=email_code)
        return redirect('/login/')
    return render(request, 'myblog/register.html', {"form": form})


def register_confirm(request):
    code = request.GET.get('code', '')
    try:
        confirm = models.ConfirmUserEmail.objects.filter(code=code).first()
        user_data = models.AdminInfo.objects.filter(username=confirm.user).first()
    except:
        message = '无效的确认请求！请检查邮件中注册地址是否正确'
        return render(request, 'myblog/register_confirm_succeed.html', {'message': message})

    c_time = confirm.c_time
    now = datetime.now()
    if now > c_time + timedelta(days=settings.CONFIRM_DAYS):
        confirm.delete()
        user_data.delete()
        message = '您的邮件已经过期，请重新注册！'
        return render(request, 'myblog/register_confirm_succeed.html', {'message': message})
    user_data.has_confirmed = True
    user_data.save()
    confirm.delete()
    message = '感谢确认，请使用账户登录！'
    return render(request, 'myblog/register_confirm_succeed.html', {'message': message})


def register_confirm_succeed(request):
    return render(request, 'myblog/register_confirm_succeed.html')


def logout(request):
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    # 调用pillow函数check_code生成图片
    img, code_string = check_code()
    # 将code_string 写入到session中，以便后续获取验证码校验
    request.session['code_string'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)
    # 写入内存(Python3)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def movie_action(request):
    return render(request, 'myblog/movie_action.html')
