from django.shortcuts import render, redirect
from myblog import models
from myblog.utils.form import UserAddModelForm
from myblog.utils.pagination import Pagination


def user_list(request):
    """用户列表"""

    users_info = models.UsersInfo.objects.all()
    users_obj = Pagination(request, users_info)
    content = {
        "users_info": users_obj.page_queryset,
        "page_str": users_obj.html()
    }
    return render(request, 'myblog/user_list.html', content)


def user_add(request):
    """添加用户"""
    if request.method == "GET":
        form = UserAddModelForm()
        return render(request, 'myblog/user_add.html', {"form": form})
    # 用户提交数据，校验，保存
    form = UserAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'myblog/user_add.html', {"form": form})


def user_edit(request, nid):
    """编辑用户"""
    # form查询可以传入字典
    # dic={'id':nid,'name'='wxm'}
    # nid_user_info = models.UsersInfo.objects.filter(**dic).first()
    nid_user_info = models.UsersInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        # 根据nid从数据库获取用户要编辑的用户信息

        form = UserAddModelForm(instance=nid_user_info)
        return render(request, 'myblog/user_edit.html', {'form': form})
    form = UserAddModelForm(data=request.POST, instance=nid_user_info)
    if form.is_valid():
        # 默认保存的是用户输入的所有的值，如果想在用户输入意外增加一些值：
        # form.instance.字段名=值
        form.save()
        return redirect('/user/list/')
    return render(request, 'myblog/user_edit.html', {"form": form})


def user_delete(request, nid):
    """删除用户"""
    models.UsersInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
