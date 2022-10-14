from django.shortcuts import render, redirect
from myblog import models
from myblog.utils.form import PrettyNumModelForm, PrettyNumEditModelForm
from myblog.utils.pagination import Pagination


def pretty_num_list(request):
    """靓号列表"""
    # 靓号搜索功能
    search_data = request.GET.get('search_num', '')  # 没有传递值。默认为空
    dic = {}
    # 手动录入100条数据
    # for _ in range(100):
    #     models.PrettyNumber.objects.create(mobile='18823333333',price=299,level=1,status=1)

    if search_data:
        dic['mobile__contains'] = search_data
    queryset = models.PrettyNumber.objects.filter(**dic).order_by('id')  # '-'表示倒序

    page_obj = Pagination(request, queryset)

    content = {
        "query_set": page_obj.page_queryset,
        "search_data": search_data,
        "page_str": page_obj.html()
    }
    return render(request, 'myblog/pretty_num_list.html', content)


def pretty_num_add(request):
    """添加靓号"""
    if request.method == 'GET':
        form = PrettyNumModelForm()
        return render(request, 'myblog/change.html', {"title": "新建靓号", "form": form})
    form = PrettyNumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty_num/list/')
    return render(request, 'myblog/change.html', {"title": "新建靓号", "form": form})


def pretty_num_edit(request, nid):
    """编辑靓号"""
    data_edit_pretty_num = models.PrettyNumber.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = PrettyNumEditModelForm(instance=data_edit_pretty_num)
        return render(request, 'myblog/change.html', {"title": "靓号编辑", "form": form})
    form = PrettyNumEditModelForm(data=request.POST, instance=data_edit_pretty_num)
    if form.is_valid():
        form.save()
        return redirect('/pretty_num/list/')
    return render(request, 'myblog/change.html', {"title": "靓号编辑", "form": form})


def pretty_num_delete(request, nid):
    models.PrettyNumber.objects.filter(id=nid).delete()
    return redirect('/pretty_num/list/')
