from django.shortcuts import render, redirect, HttpResponse
from myblog.models import AdminInfo
from myblog.utils.pagination import Pagination
from myblog.utils.form import AdminAddModelForm, AdminEditModelForm, AdminResetModelForm


def admin_list(request):
    """管理员列表"""
    info=request.session.get('info')
    print(info)
    search_username=request.GET.get("search_username", '')
    dic={}
    if search_username:
        dic['username__contains']=search_username

    query_set = AdminInfo.objects.filter(**dic)
    queryset_obj = Pagination(request, query_set)
    content = {
        "query_set": queryset_obj.page_queryset,
        "page_str": queryset_obj.html(),
        "search_username": search_username

    }
    return render(request, 'myblog/admin_list.html', content)


def admin_add(request):
    """添加管理员"""
    if request.method == 'GET':
        form = AdminAddModelForm()
        return render(request, 'myblog/change.html', {"form": form, "title": "新建管理员"})

    form = AdminAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'myblog/change.html', {"form": form, "title": "新建管理员"})


def admin_edit(request, nid):
    data_admin_edit = AdminInfo.objects.filter(id=nid).first()
    if not data_admin_edit:
        return render(request, 'myblog/error_page.html')
    title = "编辑管理员"
    if request.method == 'GET':
        form = AdminEditModelForm(instance=data_admin_edit)
        return render(request, 'myblog/change.html', {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=data_admin_edit)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'myblog/change.html', {"form": form, "title": title})


def admin_delete(request, nid):
    """删除管理员"""
    AdminInfo.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    data_admin_reset = AdminInfo.objects.filter(id=nid).first()
    if not data_admin_reset:
        return render(request, 'myblog/error_page.html')
    title = '重置{}密码'.format(data_admin_reset.username)
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'myblog/change.html', {'form': form, 'title': title})
    form = AdminResetModelForm(data=request.POST, instance=data_admin_reset)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'myblog/change.html', {'form': form, 'title': title})
