from django.shortcuts import render,redirect
from .models import Post
from datetime import datetime


# Create your views here.

def main_show(request):
    posts = Post.objects.all()
    now = datetime.now()
    return render(request, 'main_show.html', locals())


def show_post(request,slug):
    try:
        post=Post.objects.filter(slug=slug).first()
        if post:
            return render(request,'post.html',locals())
    except:
        return redirect('/main_show/')