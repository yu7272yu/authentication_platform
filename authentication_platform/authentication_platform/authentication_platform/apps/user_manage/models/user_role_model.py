# coding=utf-8
from django.db import models

from user_manage.models.base_model import BaseModel


class UserRoleModel(BaseModel):
    role_name = models.CharField(max_length=32, verbose_name='角色名称')
    description = models.TextField(verbose_name='角色描述', blank=True)

    class Meta:
        db_table = 'sh_user_role'
