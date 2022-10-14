from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    return render(request, 'myblog/chart_list.html')


def chart_bar(request):
    result = {
        'status': True,
        'legend': ['王潇猛', '季冬琴'],
        'xAxis': ['1月', '3月', '5月', '7月', '9月', '11月'],
        'series': [
            {
                'name': '王潇猛',
                'type': 'bar',
                'data': [5, 20, 36, 10, 10, 100]
            },
            {
                'name': '季冬琴',
                'type': 'bar',
                'data': [34, 110, 46, 79, 79, 60]
            },
        ]
    }
    return JsonResponse(result)


def chart_pie(request):
    result = {
        'status': True,
        'series': [
            {'value': 1048, 'name': '王潇猛'},
            {'value': 735, 'name': '季冬琴'},
            {'value': 580, 'name': '吴亚楠'},
            {'value': 484, 'name': '杨聪'},
            {'value': 300, 'name': '徐冉'}
        ],
    }
    return JsonResponse(result)


def chart_line(request):
    result = {
        'status': True,
        'series': [820, 932, 901, 934, 1290, 1330, 1320]
    }
    return JsonResponse(result)
