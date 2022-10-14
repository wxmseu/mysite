# import os
# from django.core.mail import send_mail
#
#
# def send_email(email, code):
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'stuffProject.settings'
#     send_mail(
#         '来自王潇猛个人网站注册的测试邮件',
#         '欢迎访问www.wxmseu.cn，这里是我的个人站点，本站专注于快乐学习内容的分享！' + code,
#         '962098431@qq.com',
#         [email], )

# #HTML格式邮件
import os
from django.core.mail import EmailMultiAlternatives


def send_email(email, code):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'stuffProject.settings'
    subject = '来自www.wxmseu.com的注册邮件确认'
    text_content = '欢迎访问www.wxmseu.com，这里是我的个人学习站点，专注于快乐知识技术的分享！您的验证码为：{}，请勿告诉他人'.format(code)
    html_content = '欢迎注册,点此链接确认"http://{}/register/confirm/?code={}"。这里是我的个人学习站点，' \
                   '专注于快乐知识技术的分享！'.format('127.0.0.1:8000', code)
    msg = EmailMultiAlternatives(subject=subject, body=text_content, to=[email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# send_email('xiaomeng23@126.com',22)

