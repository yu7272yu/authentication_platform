# coding=utf-8
from django.db import models

from user_manage.models.base_model import BaseModel


class UserInfoModel(BaseModel):
    phone_number = models.CharField(max_length=16, verbose_name='手机号码', blank=True)
    user_name = models.CharField(max_length=32, verbose_name='用户名称', blank=True)
    avatar_link = models.CharField(max_length=256, verbose_name='用户头像', blank=True)
    account = models.CharField(max_length=32, verbose_name='登录账户', unique=True)
    password = models.TextField(verbose_name='登录密码')
    registration_mark = models.IntegerField(verbose_name='注册来源')
    wechat = models.CharField(max_length=32, verbose_name='微信号码')
    openid = models.CharField(max_length=32, verbose_name='微信OPENID')
    email = models.CharField(max_length=32, verbose_name='企业邮箱')
    mark = models.TextField(verbose_name='备注信息')
    sh_enterprise_info = models.ManyToManyField(to='enterprise_manage.EnterpriseInfoModel', through='user_manage.UserInfoEnterpriseInfoModel')
    sh_node_info = models.ManyToManyField(to='product_manage.NodeInfoModel', through='user_manage.UserInfoNodeInfoModel')
    sh_notice_info = models.ManyToManyField(to='system_manage.NoticeInfoModel', through='user_manage.UserInfoNoticeInfoModel')

    class Meta:
        db_table = 'sh_user_info'


