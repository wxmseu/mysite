from django.shortcuts import render
import random
from django.http import JsonResponse


def choices(request):
    return render(request, 'myblog/choices.html')


def shuangseqiu(request):
    red_box = [i for i in range(1, 34)]
    blue_box = [i for i in range(1, 17)]
    red_balls = random.sample(red_box, 6)
    red_balls.sort()
    blue_balls = random.sample(blue_box, 1)
    choice_str = 'red balls：' + '，'.join(map(str, red_balls)) + '  ' + "blue balls：" + '，'.join(map(str, blue_balls))
    return JsonResponse({'message': choice_str})


def daletou(request):
    red_box = [i for i in range(1, 36)]
    blue_box = [i for i in range(1, 13)]
    red_balls = random.sample(red_box, 5)
    red_balls.sort()
    blue_balls = random.sample(blue_box, 2)
    blue_balls.sort()
    choice_str = 'front area：' + '，'.join(map(str, red_balls)) + '  ' + "back area：" + '，'.join(map(str, blue_balls))
    return JsonResponse({'message': choice_str})
