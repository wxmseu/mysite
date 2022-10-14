# Generated by Django 4.1.1 on 2022-10-09 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_boos'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=16, verbose_name='城市')),
                ('population', models.IntegerField(verbose_name='人口')),
                ('logo', models.FileField(max_length=128, upload_to='city/', verbose_name='图标')),
            ],
        ),
    ]