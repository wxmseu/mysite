from myblog import models
from django import forms
import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from myblog.utils.bootstrap import BootstrapModelForm, BootstrapForm
from myblog.utils.encrypt import md5


# 定义用户表的modelform类
# Meta 参数
# class Meta:
#     model             # 对应Model的表名
#     fields            # 需要显示的字段，“__all__”代表所有字段，也可以写成元组或列表方式
#     exclude           # 排除的字段，后面跟列表或元组
#     labels            # 提示信息，后面跟字典
#     help_texts        # 帮助提示信息，后面跟字典
#     widgets           # 自定义插件，需要先导入widgets模块

class UserAddModelForm(BootstrapModelForm):
    password = forms.CharField(min_length=6, help_text="密码位数至少要6位")

    class Meta:
        model = models.UsersInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'depart', 'gender']


# 1. MaxValueValidator ：验证最大值。
# 2. MinValueValidator ：验证最小值。
# 3. MinLengthValidator ：验证最小长度。
# 4. MaxLengthValidator ：验证最大长度。
# 5. EmailValidator ：验证是否是邮箱格式。
# 6. URLValidator ：验证是否是 URL 格式。
# 7. RegexValidator ：如果还需要更加复杂的验证，那么我们可以通过正则表达式的验证。
class PrettyNumModelForm(BootstrapModelForm):
    # 验证方法一
    # mobile=forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{10}$', '请输入正确的11位手机号')]
    # )

    class Meta:
        model = models.PrettyNumber
        # fields = ['mobile','price','level','status']
        fields = '__all__'  # 所有字段
        # exclude=['level']      # 除了某一个字段

    # 验证方法二
    def clean_mobile(self):
        text_mobile = self.cleaned_data['mobile']  # 获取用户输入的mobile手机号
        pattern = re.compile(r'^1[3-9]\d{9}$')  # 手机号的正则模板
        data_pretty_num = models.PrettyNumber.objects.filter(mobile=text_mobile).exists()  # 尝试获取数据库中是否有此手机号
        if data_pretty_num:
            raise ValidationError("该手机号已经存在")
        if not pattern.match(text_mobile):
            raise ValidationError("格式错误")  # 如果验证不通过，就抛出异常，需从django.core.exceptions引入ValidationError
        return text_mobile  # 验证通过，返回原值


class PrettyNumEditModelForm(BootstrapModelForm):
    # 手机号不可修改
    # mobile=forms.CharField(label='手机号码',disabled=True)
    class Meta:
        model = models.PrettyNumber
        # fields = ['mobile','price','level','status']
        fields = '__all__'  # 所有字段
        # exclude=['level']      # 除了某一个字段

    def clean_mobile(self):
        text_mobile = self.cleaned_data['mobile']  # 获取用户输入的mobile手机号
        pattern = re.compile(r'^1[3-9]\d{9}$')  # 手机号的正则模板
        # 与添加靓号验证规则不同，应排除自身，用exclude排除，self.instance.pk获取自身的primary key
        data_pretty_num = models.PrettyNumber.objects.filter(mobile=text_mobile).exclude(id=self.instance.pk).exists()
        if data_pretty_num:
            raise ValidationError("该手机号已经存在")
        if not pattern.match(text_mobile):
            raise ValidationError("格式错误")  # 如果验证不通过，就抛出异常，需从django.core.exceptions引入ValidationError
        return text_mobile  # 验证通过，返回原值


class AdminAddModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        max_length=64,
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.AdminInfo
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            # 密码保留原来的值并隐藏
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_username(self):
        text_username = self.cleaned_data['username']
        data_username = models.AdminInfo.objects.filter(username=text_username).exists()
        if data_username:
            raise ValidationError("用户名已经存在")
        return text_username

    def clean_password(self):
        return md5(self.cleaned_data.get('password'))

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = md5(self.cleaned_data["confirm_password"])
        if password != confirm_password:
            raise ValidationError("两次密码输入不一致，请重新输入")
        return confirm_password


class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.AdminInfo
        fields = ['username']
        # fields = ['username', 'password']   # 默认设置不可修改密码


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        max_length=64,
        widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.AdminInfo
        fields = ['password', 'confirm_password']
        widgets = {
            # 密码保留原来的值
            "password": forms.PasswordInput(render_value=True),
            'confirm_password': forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        # 判断新输入的密码是否与数据库中的原密码相同
        md5_pwd = md5(self.cleaned_data.get('password'))
        old_pwd = models.AdminInfo.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if old_pwd:
            raise ValidationError('新密码不能与原密码相同')
        return md5_pwd

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))
        if password != confirm_password and password is not None:
            raise ValidationError("两次密码输入不一致，请重新输入")
        return confirm_password


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True

    )

    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            "content": forms.TextInput
            # "detail":forms.Textarea
        }


class OrderModelForm(BootstrapModelForm):
    order_num = forms.CharField(label='订单号', disabled=True, required=False)

    class Meta:
        model = models.Orders
        fields = '__all__'
        # exclude = ['order_num']


class RegisterModelForm(BootstrapModelForm):
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True,
    )
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True
    )

    class Meta:
        model = models.AdminInfo
        fields = '__all__'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = models.AdminInfo.objects.filter(username=username).first()
        if user:
            raise ValidationError('用户名已存在')
        return username

    def clean_password(self):
        return md5(self.cleaned_data.get('password'))

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        pwd = self.cleaned_data.get('password')
        if md5(confirm_password) != pwd:
            raise ValidationError('两次输入密码不一致')
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        obj = re.compile(
            r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?")
        if not obj.match(email):
            raise ValidationError('邮箱格式不正确')
        user_email = models.AdminInfo.objects.filter(email=email).first()
        if user_email:
            if user_email.has_confirmed == 0:
                raise ValidationError('该邮箱已注册但未确认，请前往注册邮箱查看')
            else:
                raise ValidationError('该邮箱已被注册')
        return email
