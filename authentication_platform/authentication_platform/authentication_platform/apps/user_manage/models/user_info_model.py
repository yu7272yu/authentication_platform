# coding=utf-8
from django.db import models

# from app_manage.models.base_model import BaseModel
from user_manage.models.base_model import BaseModel


class UserInfoModel(BaseModel):
    user_name = models.CharField(max_length=32, verbose_name='用户账号')
    # user_name = models.BinaryField(verbose_name='用户账号')
    user_password = models.CharField(max_length=128, verbose_name='用户密码')
    email = models.CharField(max_length=32, blank=True, verbose_name='邮箱信息')
    telephone = models.CharField(max_length=16, blank=True, verbose_name='手机号码')
    nickname = models.CharField(max_length=32, blank=True, verbose_name='用户昵称')
    avatar_url = models.CharField(max_length=128, blank=True, verbose_name='头像地址')
    sh_user_role = models.ForeignKey(to='UserRoleModel', on_delete=models.PROTECT, verbose_name='用户角色id')
    # sh_alarm_info = models.ManyToManyField(to='app_manage.AlarmInfoModel', through='app_manage.ShUserInfoShAlarmInfo', verbose_name='警告信息')
    # app_info = models.ManyToManyField(to='app_manage.AppInfoModel')

    class Meta:
        db_table = 'sh_user_info'


