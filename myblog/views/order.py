from django.shortcuts import render, HttpResponse
from myblog.utils.form import OrderModelForm
from myblog import models
from myblog.utils.pagination import Pagination
from django.views.decorators.csrf import csrf_exempt
import time
from django.http import JsonResponse


def order_list(request):
    query_set = models.Orders.objects.all().order_by('-id')
    page_obj = Pagination(request, query_set)
    form = OrderModelForm()
    content = {
        "form": form,
        "query_set": page_obj.page_queryset,
        "page_str": page_obj.html()
    }
    return render(request, 'myblog/order_list.html', content)


@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 将当前时间作为订单号
        form.instance.order_num = time.strftime("%Y%m%d%H%M%S")

        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors.get_json_data()})


@csrf_exempt
def order_edit(request):
    uid=request.GET.get('uid')
    row_obj=models.Orders.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({"status": False, 'error': '修改失败，数据不存在！'})
    form = OrderModelForm(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors.get_json_data()})


@csrf_exempt
def order_delete(request):
    uid = request.POST.get('uid')
    exists = models.Orders.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': '删除失败，数据不存在！'})
    models.Orders.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    uid = request.GET.get('uid')
    data = models.Orders.objects.filter(id=uid).values('order_num', 'good_name', 'price', 'status', 'user').first()
    if not data:
        return JsonResponse({"status": False, 'error': '修改失败，数据不存在！'})
    result = {
        'status': True,
        'data': data
    }
    return JsonResponse(result)
