from django.shortcuts import render


def practice(request):
    return render(request, 'myblog/practice.html')


def dynamic_content(request):
    return render(request, 'myblog/dynamic_content.html')
