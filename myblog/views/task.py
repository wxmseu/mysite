import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from myblog.utils.form import TaskModelForm
from myblog import models
from myblog.utils.pagination import Pagination


def task_list(request):
    """任务列表"""
    query_set=models.Task.objects.all().order_by('id')
    form = TaskModelForm()
    page_obj=Pagination(request, query_set,pagesize=5)
    content={
        "form": form,
        "query_set":page_obj.page_queryset,
        "page_str": page_obj.html()
    }
    return render(request, 'myblog/task_ajax.html', content)


@csrf_exempt  # 免除csrf验证
def task_ajax(request):
    print(request.POST)
    data_dic = {"name": 'wmx', 'data': [1, 23, 4, 5, 5, 6]}
    # 两种返回json格式的写法，1：json.dumps()    2:JsonResponse(data_dic)
    # data_str=json.dumps(data_dic)
    # return HttpResponse(data_str)
    return JsonResponse(data_dic)


@csrf_exempt
def task_add(request):
    # 1.用户发来的数据进行校验（用modelform）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dic = {"status": True}
        return HttpResponse(json.dumps(data_dic))
    # print(type(form.errors))
    data_dic = {"status": False, "error": form.errors.get_json_data()}
    # print(form.errors.get_json_data())
    return HttpResponse(json.dumps(data_dic))
