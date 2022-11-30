# coding=utf-8
from django.db import models

from user_manage.models.base_model import BaseModel


class UserInfoEnterpriseInfoModel(BaseModel):
    show_flag = models.IntegerField(verbose_name='显示表示')
    sh_user_info = models.ForeignKey(to='user_manage.UserInfoModel', on_delete=models.PROTECT, verbose_name='用户id')
    sh_enterprise_info = models.ForeignKey(to='enterprise_manage.EnterpriseInfoModel', on_delete=models.PROTECT, verbose_name='企业id')

    class Meta:
        db_table = 'sh_user_info_sh_enterprise_info'
