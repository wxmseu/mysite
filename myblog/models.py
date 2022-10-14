from django.db import models


# Create your models here.
class AdminInfo(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=64)
    gender_choice = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class ConfirmUserEmail(models.Model):
    code = models.CharField(verbose_name='邮箱验证码', max_length=256)
    user = models.CharField(verbose_name='用户名', max_length=32)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user + ":   " + self.code


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.title


class UsersInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # create_time=models.DateTimeField(verbose_name='入职时间')
    create_time = models.DateField(verbose_name='入职时间')

    # 无约束
    # depart_id=models.BigIntegerField(verbose_name='部门id')
    # 1.有约束
    #   -to 与那张表关联
    #   -to_field 表中的那一列关联
    # 2. django自动
    #   -写的depart
    #   -生成数据列 depart_id
    # 3. 部门表被删除
    #       3.1级联删除
    depart = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', on_delete=models.CASCADE)
    #       3.2级联删除
    # depart = models.ForeignKey(verbose_name='部门id', to='Department', to_field='department',null=True,
    # blank=True, on_delete=models.SET_NULL())

    # django中的约束
    gender_choice = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)

    def __str__(self):
        return self.name


class PrettyNumber(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    # 想要为空，null=True,blank=True
    price = models.IntegerField(verbose_name='价格', default=0)
    level_choices = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)
    status_choices = (
        (1, '已占用'),
        (2, '未占用')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=2)


class Task(models.Model):
    level_choice = (
        (1, "紧急"),
        (2, "一般"),
        (3, "临时")
    )
    level = models.SmallIntegerField(verbose_name="重要等级", choices=level_choice, default=2)
    title = models.CharField(verbose_name='标题', max_length=64)
    content = models.TextField(verbose_name='任务详情')
    user = models.ForeignKey(verbose_name="负责人", to=AdminInfo, on_delete=models.CASCADE)


class Orders(models.Model):
    order_num = models.CharField(verbose_name='订单号', max_length=32)
    good_name = models.CharField(verbose_name='商品名称', max_length=16)
    price = models.IntegerField(verbose_name='价格')
    status_choice = (
        (1, "已支付"),
        (2, "未支付")
    )
    status = models.SmallIntegerField(verbose_name="支付状态", choices=status_choice, default=2)
    user = models.ForeignKey(verbose_name="买家用户", to=UsersInfo, on_delete=models.CASCADE)


class Boos(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    img = models.CharField(verbose_name='头像', max_length=64)


class City(models.Model):
    city = models.CharField(verbose_name='城市', max_length=16)
    population = models.IntegerField(verbose_name='人口')
    logo = models.FileField(verbose_name='图标', max_length=128, upload_to='city/')
