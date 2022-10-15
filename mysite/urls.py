"""stuffProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django import contrib
from mainsite import views

from django.views.static import serve
from django.urls import re_path
from django.urls import path
from mysite import settings
from myblog.views import depart, homepage, pretty_num, user, admin, task, order, choice, practice, chart, upload

urlpatterns = [
    path('admin/', contrib.admin.site.urls),
    path('main_show/', views.main_show),
    path('post/<slug:slug>/', views.show_post),

    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # 首页和登录页面
    path('', homepage.homepage),
    path('login/', homepage.login),
    path('register/', homepage.register),
    path('register/confirm/', homepage.register_confirm),
    path('register/confirm/succeed', homepage.register_confirm_succeed),
    path('logout/', homepage.logout),
    path('image/code/', homepage.image_code),
    path('movie/action/', homepage.movie_action),

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),
    path('depart/upload/', depart.depart_upload),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # 靓号管理
    path('pretty_num/list/', pretty_num.pretty_num_list),
    path('pretty_num/add/', pretty_num.pretty_num_add),
    path('pretty_num/<int:nid>/edit/', pretty_num.pretty_num_edit),
    path('pretty_num/<int:nid>/delete/', pretty_num.pretty_num_delete),

    # 任务管理
    path('task/list/', task.task_list),
    path('task/ajax/', task.task_ajax),
    path('task/add/', task.task_add),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),

    # 选号
    path('choices/', choice.choices),
    path('shuangseqiu/', choice.shuangseqiu),
    path('daletou/', choice.daletou),

    # 各种练习
    path('practice/', practice.practice),
    path('dynamic_content/', practice.dynamic_content),
    path('eat_what/', practice.eat_what),

    # 上传文件
    path('upload/form/', upload.upload_form),
    path('upload/modelform/', upload.upload_modelform),

]
