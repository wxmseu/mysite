from django.shortcuts import render, redirect
from myblog.utils.bootstrap import BootstrapForm, BootstrapModelForm
from django import forms
import os
from myblog import models
from mysite import settings
from django.conf import settings


# def upload_list(request):
#     if request.method == 'GET':
#         return render(request, 'upload_form.html')
#     # print(request.POST)
#     # print(request.FILES)
#     file_obj = request.FILES.get('file_content')
#     f = open(file_obj.name, mode='wb')
#     for chunk in file_obj.chunks():
#         f.write(chunk)
#     f.close()
#     return HttpResponse('chenggngle')

class UploadForm(BootstrapForm):
    bootstrap_exclude_fields = ['img_head']
    username = forms.CharField(label='用户名', max_length=16)
    age = forms.IntegerField(label='年龄')
    img_head = forms.FileField(label='头像')


def upload_form(request):
    title = 'form上传'
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'myblog/upload_form.html', {'form': form, 'title': title})
    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 1.读取用户上传的文件，将其保存到本地文件夹，获取存储的路径
        img_obj = form.cleaned_data['img_head']
        # media_path = os.path.join(settings.MEDIA_URL, img_obj.name)
        media_path = os.path.join('media', img_obj.name)

        f = open(media_path, 'wb')
        for chunk in img_obj.chunks():
            f.write(chunk)
        f.close()
        # 2. 将路径保存到数据库中
        models.Boos.objects.create(
            name=form.cleaned_data['username'],
            age=form.cleaned_data['age'],
            img=media_path
        )
        return redirect('/upload/form/')
    return render(request, 'myblog/upload_form.html', {'form': form, 'title': title})


class UploadModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['logo']

    class Meta:
        model = models.City
        fields = '__all__'


def upload_modelform(request):
    title = 'modelform上传'
    city_list=models.City.objects.all()
    if request.method == 'GET':
        form = UploadModelForm()
        return render(request, 'myblog/upload_form.html', {'form': form, 'title': title, 'city_list':city_list})
    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/upload/modelform/')
    return render(request, 'myblog/upload_form.html', {'form': form, 'title': title, 'city_list': city_list})
